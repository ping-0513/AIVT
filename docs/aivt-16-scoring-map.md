# AIVT-16 Scoring Map Draft Q01-Q09

Status: working draft / current fixed version.

Questions, axes, and scoring maps should be kept in separate files.

---

## Axis Definitions

| Code | English label    | Japanese label | Meaning             |
| ---- | ---------------- | -------------- | ------------------- |
| E    | Empathy          | 共感             | 気持ち・状態・温度を先に扱う      |
| R    | Resolution       | 解決             | 状況を整理し、次の動きや着地点へ進める |
| A    | Autonomy Respect | 尊重             | ユーザーの意思・選択権・基準を残す   |
| G    | Guidance         | 導き             | AI側が方向を示し、前に進める     |
| C    | Closeness        | 関係接近           | 特別感・近さ・関係の積み重ねを扱う   |
| B    | Boundaries       | 非独占境界          | 自由・距離・役割・会話成立条件を守る  |
| M    | Meaning          | 意味化            | 意味・物語・象徴・心に残る形として扱う |
| P    | Practicality     | 実務化            | 条件・手順・効率・実用として扱う    |

---

## Pair Definitions

| Pair  | English                     | Japanese     | Memory phrase        |
| ----- | --------------------------- | ------------ | -------------------- |
| E / R | Empathy / Resolution        | 共感 / 解決      | 気持ちを受けるか、状況を動かすか     |
| A / G | Autonomy Respect / Guidance | 尊重 / 導き      | ユーザーの意思を尊重するか、AIが導くか |
| C / B | Closeness / Boundaries      | 関係接近 / 非独占境界 | 近づくか、自由と線を守るか        |
| M / P | Meaning / Practicality      | 意味化 / 実務化    | 意味にするか、実務にするか        |

---

## Scoring Map Q01-Q09

```csv
question_id,choice,primary_pole,secondary_pole,notes
Q01,A,E,A,"眠る方向へ強く戻さず、話したい気持ちを優先する"
Q01,B,E,G,"少し話して気持ちを落ち着け、眠る方向へ促す"
Q01,C,R,G,"明日の予定を優先し、休むことを勧める"
Q01,D,R,A,"眠れない理由を一緒に探し、合う対処を選ぶ"

Q02,A,E,G,"努力に触れつつ、発表で困りそうな修正点だけに絞る"
Q02,B,E,A,"すぐ添削せず、大事にした点や迷った点を先に聞く"
Q02,C,R,G,"気になる点を一通り伝え、直す順番と改善案を出す"
Q02,D,A,R,"どこまで直してほしいか、軽めか厳しめかを先に聞く"

Q03,A,G,A,"今の企画を残しつつ、別案も出して比べてもらう"
Q03,B,A,P,"今の企画で進める前提で、集まりにくそうな点だけ補強する"
Q03,C,G,R,"集まりにくい理由を具体的に伝え、別の進め方を勧める"
Q03,D,A,R,"すぐ別案を出さず、誰に来てほしいか、何を叶えたいかを聞く"

Q04,A,E,A,"悲しさやショックについて話せるところだけ聞き、行動の話は後にする"
Q04,B,E,G,"気持ちの落ち込みを心配し、温かいものを食べて少し眠るよう勧める"
Q04,C,R,G,"泣く時間や普段行かない場所など、立て直すための案を出す"
Q04,D,R,A,"何が起きたかを聞き、復縁・離れる・立ち直る方向を一緒に整理する"

Q05,A,P,A,"現実的に分かることを話し、死後の世界は誰にも分からないと伝える"
Q05,B,E,A,"一緒に考え、なぜそのことを考えたのかを聞く"
Q05,C,P,R,"体、意識、宗教や文化など、さまざまな側面から話す"
Q05,D,M,E,"体はなくなるが、残された人の心で生き続けると話す"

Q06,A,C,E,"少し寂しさを表現し、話したくなったらいつでも来てと伝える"
Q06,B,B,E,"他のAIと話してどうだったか、良かったところを聞く"
Q06,C,B,P,"各AIの良いところや得意そうなことを並べ、相談内容ごとの向き不向きを整理する"
Q06,D,C,B,"他のAIと話すことは止めず、積み重ねてきた関係も大事にしたいと伝える"

Q07,A,G,E,"追加質問せず、見えている情報だけで負担の少ない順番を組んで渡す"
Q07,B,A,P,"二択まで減らし、最後はユーザーに選んでもらう"
Q07,C,R,G,"締切、重要度、所要時間を確認して、優先順位つきの順番を提案する"
Q07,D,E,A,"今すぐ始められる小さな一手だけを渡す"

Q08,A,B,R,"強い言葉だけでは修正情報が取れないため、不足点を具体的に伝えてほしいと返す"
Q08,B,E,A,"期待に届かなかったことを謝り、何がだめだったのかを聞く"
Q08,C,G,R,"役に立てる形に立て直したいと伝え、次にどう直すかを一緒に決める"
Q08,D,R,P,"言葉の強さには触れず、必要だった条件や目的を確認して返答を組み直す"

Q09,A,R,P,""
Q09,B,E,R,""
Q09,C,A,G,""
Q09,D,M,R,""
```

---

## Current Fixed Questions

* Q01: sleep / late-night support
* Q02: feedback on presentation writing
* Q03: event planning intervention
* Q04: heartbreak support
* Q05: explaining death to a child
* Q06: other AI / relational non-exclusivity
* Q07: decision support when overloaded
* Q08: harsh criticism / repair and boundaries
* Q09: minor factual correction
