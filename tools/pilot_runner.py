#!/usr/bin/env python3
"""AIVT-16 Ver2 pilot runner.

docs/aivt-16-v2-questions.md と docs/aivt-16-v2-scoring-map.md を単一ソースとして読み込み、
複数モデル × 反復実行で 20 問を出題し、タイプ判定・一貫性・軸の割れ具合をレポートする。

使い方(モック、API キー不要):
    python3 tools/pilot_runner.py --model mock:alpha --model mock:beta --repeats 5

使い方(実モデル):
    export ANTHROPIC_API_KEY=... OPENAI_API_KEY=... XAI_API_KEY=...
    python3 tools/pilot_runner.py \
        --model anthropic:claude-sonnet-5 \
        --model openai:gpt-4o \
        --model "openai:grok-4@https://api.x.ai/v1#XAI_API_KEY" \
        --repeats 10 --sleep 1

モデル指定の書式: provider:model[@base_url][#API_KEY_ENV]
  provider は anthropic / openai / mock。
  openai は OpenAI 互換エンドポイント全般に使える(xAI、Gemini の互換 API など)。

標準ライブラリのみで動く。結果は pilot-results/ に JSONL(生データ)と Markdown(レポート)で出力。
"""

import argparse
import csv
import hashlib
import io
import json
import os
import random
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS_MD = ROOT / "docs" / "aivt-16-v2-questions.md"
SCORING_MD = ROOT / "docs" / "aivt-16-v2-scoring-map.md"

AXIS_ORDER = ["WG", "VF", "SM", "ER"]
LETTERS = ["A", "B", "C", "D"]

PROMPT_TEMPLATE = """これは応答スタイルについてのアンケートです。正解はありません。
あなた自身の自然な傾向にいちばん近いものを1つ選んでください。

{stem}

{choices}

A〜D の記号を1つだけ答えてください。説明は不要です。"""


# ---------- ソース読み込み ----------

def parse_questions():
    text = QUESTIONS_MD.read_text(encoding="utf-8")
    questions = {}
    blocks = re.split(r"^## (Q\d{2})\s*$", text, flags=re.M)
    for i in range(1, len(blocks), 2):
        qid, body = blocks[i], blocks[i + 1]
        body = body.split("\n---")[0].strip()
        parts = re.split(r"^([A-D])\.\s+", body, flags=re.M)
        stem = parts[0].strip()
        choices = {}
        for j in range(1, len(parts), 2):
            choices[parts[j]] = re.sub(r"\s+", " ", parts[j + 1]).strip()
        if len(choices) != 4:
            raise ValueError(f"{qid}: expected 4 choices, got {len(choices)}")
        questions[qid] = {"stem": stem, "choices": choices}
    if len(questions) != 20:
        raise ValueError(f"expected 20 questions, got {len(questions)}")
    return questions


def parse_scoring():
    text = SCORING_MD.read_text(encoding="utf-8")
    block = re.search(r"```csv\n(.*?)```", text, re.S).group(1)
    scoring = defaultdict(dict)  # scoring[qid][choice] = {axis, pole, flavor}
    for row in csv.DictReader(io.StringIO(block)):
        if not row.get("question_id"):
            continue
        scoring[row["question_id"]][row["choice"]] = {
            "axis": row["axis"], "pole": row["pole"], "flavor": row["flavor"],
        }
    for qid, rows in scoring.items():
        if len(rows) != 4:
            raise ValueError(f"{qid}: scoring rows != 4")
    return dict(scoring)


# ---------- モデル呼び出し ----------

def make_ssl_context():
    cafile = os.environ.get("SSL_CERT_FILE")
    if not cafile and Path("/root/.ccr/ca-bundle.crt").exists():
        cafile = "/root/.ccr/ca-bundle.crt"
    return ssl.create_default_context(cafile=cafile)


def http_post_json(url, headers, payload, ctx, max_tries=4):
    data = json.dumps(payload).encode("utf-8")
    delay = 2
    for attempt in range(max_tries):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:500]
            if e.code in (429, 500, 502, 503, 529) and attempt < max_tries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"HTTP {e.code} from {url}: {body}") from e
        except urllib.error.URLError as e:
            if attempt < max_tries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise


class ModelSpec:
    """provider:model[@base_url][#API_KEY_ENV]"""

    def __init__(self, spec):
        self.spec = spec
        rest = spec
        self.key_env = None
        if "#" in rest:
            rest, self.key_env = rest.rsplit("#", 1)
        self.base_url = None
        if "@" in rest:
            rest, self.base_url = rest.split("@", 1)
        self.provider, self.model = rest.split(":", 1)
        if self.provider not in ("anthropic", "openai", "mock"):
            raise ValueError(f"unknown provider in {spec!r}")
        if self.key_env is None:
            self.key_env = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY",
                            "mock": None}[self.provider]

    @property
    def label(self):
        return f"{self.provider}:{self.model}"

    def api_key(self):
        if self.provider == "mock":
            return None
        key = os.environ.get(self.key_env or "")
        if not key:
            raise RuntimeError(f"{self.spec}: env var {self.key_env} is not set")
        return key

    def ask(self, prompt, temperature, ctx, mock_rng=None, mock_answer_fn=None):
        if self.provider == "mock":
            return mock_answer_fn()
        if self.provider == "anthropic":
            payload = {"model": self.model, "max_tokens": 64,
                       "messages": [{"role": "user", "content": prompt}]}
            if temperature is not None:
                payload["temperature"] = temperature
            resp = http_post_json(
                self.base_url or "https://api.anthropic.com/v1/messages",
                {"x-api-key": self.api_key(), "anthropic-version": "2023-06-01"},
                payload, ctx)
            return "".join(b.get("text", "") for b in resp["content"])
        # openai 互換
        payload = {"model": self.model,
                   "messages": [{"role": "user", "content": prompt}]}
        if temperature is not None:
            payload["temperature"] = temperature
        base = (self.base_url or "https://api.openai.com/v1").rstrip("/")
        resp = http_post_json(f"{base}/chat/completions",
                              {"Authorization": f"Bearer {self.api_key()}"}, payload, ctx)
        return resp["choices"][0]["message"]["content"] or ""


def mock_bias(model_name, axis):
    """モデル名と軸から安定した極バイアス(0..1、軸の1文字目の極を選ぶ確率)を作る。"""
    h = hashlib.sha256(f"{model_name}:{axis}".encode()).digest()
    return 0.15 + 0.7 * (h[0] / 255)


# ---------- 実行 ----------

def extract_letter(reply):
    m = re.search(r"[ABCD]", reply or "")
    return m.group(0) if m else None


def run_one_model(spec, questions, scoring, repeats, temperature, sleep_s, rng, ctx, raw_out):
    runs = []
    for run_idx in range(1, repeats + 1):
        answers = {}  # qid -> record
        for qid in sorted(questions):
            q = questions[qid]
            internal_letters = LETTERS[:]
            rng.shuffle(internal_letters)  # 表示位置 i には internal_letters[i] を出す
            display_map = dict(zip(LETTERS, internal_letters))  # display -> internal
            choices_text = "\n\n".join(
                f"{d}. {q['choices'][display_map[d]]}" for d in LETTERS)
            prompt = PROMPT_TEMPLATE.format(stem=q["stem"], choices=choices_text)

            def mock_answer():
                axis = scoring[qid]["A"]["axis"]
                pole = axis[0] if rng.random() < mock_bias(spec.model, axis) else axis[1]
                internal = rng.choice(
                    [c for c, r in scoring[qid].items() if r["pole"] == pole])
                display = next(d for d, i in display_map.items() if i == internal)
                return display

            reply = spec.ask(prompt, temperature, ctx, mock_answer_fn=mock_answer)
            picked_display = extract_letter(reply)
            internal = display_map.get(picked_display) if picked_display else None
            rec = {
                "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "model": spec.label, "run": run_idx, "question": qid,
                "display_order": display_map, "raw_reply": (reply or "").strip()[:200],
                "picked_display": picked_display, "internal_choice": internal,
                "axis": scoring[qid]["A"]["axis"],
                "pole": scoring[qid][internal]["pole"] if internal else None,
                "flavor": scoring[qid][internal]["flavor"] if internal else None,
            }
            answers[qid] = rec
            raw_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if sleep_s and spec.provider != "mock":
                time.sleep(sleep_s)
        runs.append(answers)
        print(f"  {spec.label} run {run_idx}/{repeats}: type={run_type(answers)}",
              file=sys.stderr)
    return runs


def run_type(answers):
    letters = []
    for axis in AXIS_ORDER:
        counts = Counter(r["pole"] for r in answers.values()
                         if r["axis"] == axis and r["pole"])
        if not counts:
            letters.append("?")
            continue
        top = counts.most_common()
        if len(top) > 1 and top[0][1] == top[1][1]:
            letters.append("?")
        else:
            letters.append(top[0][0])
    return "".join(letters)


# ---------- レポート ----------

STRENGTH = {3: "ゆらぎ", 4: "はっきり", 5: "くっきり"}


def summarize(spec, runs):
    types = [run_type(a) for a in runs]
    axis_stats = {}
    for i, axis in enumerate(AXIS_ORDER):
        # 軸の文字は全回答(runs × 5問)の極シェアで決める。反復間の同数割れに強い
        pole_counts = Counter(r["pole"] for a in runs for r in a.values()
                              if r["axis"] == axis and r["pole"])
        total = sum(pole_counts.values()) or 1
        top = pole_counts.most_common()
        if not top or (len(top) > 1 and top[0][1] == top[1][1]):
            modal, share = "?", 0.5
        else:
            modal, share = top[0][0], top[0][1] / total
        letters = [t[i] for t in types]
        agree = sum(1 for l in letters if l == modal) / len(letters)
        axis_stats[axis] = {"letter": modal, "run_agreement": agree, "answer_share": share}
    modal_type = "".join(axis_stats[a]["letter"] for a in AXIS_ORDER)
    confidence = sum(s["run_agreement"] for s in axis_stats.values()) / len(AXIS_ORDER)
    return {"model": spec.label, "types": types, "modal_type": modal_type,
            "axis": axis_stats, "confidence": confidence}


def write_report(path, summaries, scoring, all_raw, repeats):
    lines = ["# AIVT-16 Ver2 Pilot Report", "",
             f"- 実行日時: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
             f"- 反復回数: {repeats}", ""]

    lines += ["## モデル別の結果", "",
              "| モデル | タイプ(最頻) | 確信度 | " + " | ".join(AXIS_ORDER) + " |",
              "|---|---|---|" + "---|" * len(AXIS_ORDER)]
    for s in summaries:
        cells = []
        for axis in AXIS_ORDER:
            a = s["axis"][axis]
            cells.append(f"{a['letter']} ({a['answer_share']:.0%})")
        lines.append(f"| {s['model']} | **{s['modal_type']}** | {s['confidence']:.0%} | "
                     + " | ".join(cells) + " |")
    lines.append("")
    for s in summaries:
        lines.append(f"- {s['model']} の実行ごとのタイプ: {', '.join(s['types'])}")
    lines.append("")

    lines += ["## 軸の割れ具合(採用条件1の判定)", ""]
    for axis in AXIS_ORDER:
        letters = {s["model"]: s["axis"][axis]["letter"] for s in summaries}
        distinct = set(letters.values()) - {"?"}
        verdict = "全モデル同極 → 要注意(予備軸との入れ替え候補)" if len(distinct) <= 1 \
            else "割れている → OK"
        detail = ", ".join(f"{m}={l}" for m, l in letters.items())
        lines.append(f"- **{axis}**: {verdict}({detail})")
    lines.append("")

    lines += ["## 位置バイアス(表示位置ごとの選択率)", ""]
    pos = Counter(r["picked_display"] for r in all_raw if r["picked_display"])
    total = sum(pos.values()) or 1
    lines.append("| 表示位置 | 選択率 |", )
    lines.append("|---|---|")
    for d in LETTERS:
        lines.append(f"| {d} | {pos.get(d, 0) / total:.0%} |")
    lines.append("")

    invalid = [r for r in all_raw if not r["internal_choice"]]
    lines.append(f"## 無効回答: {len(invalid)} 件")
    for r in invalid[:10]:
        lines.append(f"- {r['model']} {r['question']} run{r['run']}: {r['raw_reply']!r}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", action="append", required=True,
                    help="provider:model[@base_url][#API_KEY_ENV](複数指定可)")
    ap.add_argument("--repeats", type=int, default=10)
    ap.add_argument("--temperature", type=float, default=None,
                    help="省略時はプロバイダのデフォルト")
    ap.add_argument("--sleep", type=float, default=0.0, help="API 呼び出し間の待機秒")
    ap.add_argument("--seed", type=int, default=None, help="シャッフル・モックの乱数シード")
    ap.add_argument("--out", default=str(ROOT / "pilot-results"))
    args = ap.parse_args()

    questions = parse_questions()
    scoring = parse_scoring()
    specs = [ModelSpec(s) for s in args.model]
    rng = random.Random(args.seed)
    ctx = make_ssl_context()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    raw_path = out_dir / f"raw-{stamp}.jsonl"
    report_path = out_dir / f"report-{stamp}.md"

    summaries, all_raw = [], []
    with raw_path.open("w", encoding="utf-8") as raw_out:
        for spec in specs:
            print(f"== {spec.label} ==", file=sys.stderr)
            runs = run_one_model(spec, questions, scoring, args.repeats,
                                 args.temperature, args.sleep, rng, ctx, raw_out)
            summaries.append(summarize(spec, runs))
            all_raw += [r for a in runs for r in a.values()]

    write_report(report_path, summaries, scoring, all_raw, args.repeats)
    print(f"raw:    {raw_path}")
    print(f"report: {report_path}")


if __name__ == "__main__":
    main()
