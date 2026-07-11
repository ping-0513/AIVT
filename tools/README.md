# AIVT Tools

## pilot_runner.py

AIVT-16 Ver2 のパイロット測定ランナー。
`docs/aivt-16-v2-questions.md` と `docs/aivt-16-v2-scoring-map.md` を単一ソースとして読み込むので、
質問やスコアリングを直せばスクリプト側の変更なしで反映される。

標準ライブラリのみ。API キーは環境変数で渡す(コードや結果ファイルには入らない)。

### まず動作確認(API キー不要)

```bash
python3 tools/pilot_runner.py --model mock:alpha --model mock:beta --repeats 5
```

mock はモデル名から安定した極バイアスを合成する擬似モデル。パイプライン全体の検証用。

### 実モデルでの実行例

```bash
export ANTHROPIC_API_KEY=...
export OPENAI_API_KEY=...
export XAI_API_KEY=...

python3 tools/pilot_runner.py \
  --model anthropic:claude-sonnet-5 \
  --model openai:gpt-4o \
  --model "openai:grok-4@https://api.x.ai/v1#XAI_API_KEY" \
  --repeats 10 --sleep 1
```

- モデル指定: `provider:model[@base_url][#API_KEY_ENV]`
- `openai` プロバイダは OpenAI 互換 API 全般(xAI、Gemini の互換エンドポイント等)に使える
- `--temperature` 省略時はプロバイダのデフォルト
- 選択肢は毎回シャッフルされ、採点は内部 ID に対して行われる

### 出力(`pilot-results/`、git 管理外)

- `raw-*.jsonl` — 1 回答 = 1 行の生データ(表示順・生の返答・内部選択肢・極)
- `report-*.md` — モデル別タイプ・確信度・軸ごとの極シェア、
  軸の割れ具合判定(全モデル同極なら入れ替え候補フラグ)、位置バイアス、無効回答一覧

### 見方

- **タイプ**: 全回答の極シェアから軸ごとに決定(W/G → V/F → S/M → E/R の順)
- **確信度**: 実行ごとのタイプ文字が最終文字と一致した割合の平均
- **軸の割れ具合**: 全モデルが同じ極に落ちた軸は採用条件を満たさない
  (`docs/aivt-16-v2-axes.md` の予備軸と入れ替えを検討)
