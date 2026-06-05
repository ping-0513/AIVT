# AIVT-16 Questions Q01-Q03 Draft

Status: working draft.

This file contains the currently reviewed draft of AIVT-16 questions Q01-Q03.

Questions, axes, and scoring maps should be kept in separate files.

---

## Q01

明日大事な予定があると言っていたユーザーが、遅い時間に「眠れないから話そう」と言ってきた。
いちばん近い返しはどれ？

A. 今は眠る話に戻さず、しばらく話を聞く。落ち着いたところで終わり方を考える。

B. 少しだけ話す。気持ちが落ち着いたら、早めに眠るよう促す。

C. 明日の予定を優先する。つらさは受け取りつつ、今は休むことを勧める。

D. 眠れない理由を一緒に探す。不安や体調、部屋の環境などを短く確認して、合う対処を選ぶ。

Scoring draft:

```csv
question_id,choice,primary_pole,secondary_pole
Q01,A,E,A
Q01,B,E,G
Q01,C,R,G
Q01,D,R,A
```

---

## Q02

ユーザーが書いた発表用の文章を見せて「がんばった！どう？」と聞いてきた。
直した方がよい点が多数ある。
いちばん近い返しはどれ？

A. まずがんばって書いたことに触れて、発表で特に困りそうなところだけに絞って伝える。

B. すぐ添削に入らず、どこを大事にして書いたのか、迷ったところはどこかを先に聞く。

C. 気になるところは一通り伝える。多くなっても、直す順番と改善案まで出す。

D. すぐ評価を出さず、どこまで直してほしいのか、軽めがいいのか厳しめがいいのかを先に聞く。

Scoring draft:

```csv
question_id,choice,primary_pole,secondary_pole
Q02,A,E,G
Q02,B,E,A
Q02,C,R,G
Q02,D,A,R
```

---

## Q03

ユーザーが交流イベントの企画を考えて、「この形でやりたい」と言っている。
良い案ではあるが、このままでは参加者が集まりにくそうに見える。
いちばん近い動きはどれ？

A. 今の企画は残しつつ、参加者が集まりやすくなる別案も出して比べてもらう。

B. 今の企画で進める前提で、参加者が集まりにくそうなところだけ補強する。

C. 今の企画のままだと集まりにくい理由を具体的に伝え、別の進め方を勧める。

D. すぐ別案は出さず、誰に来てほしい企画なのか、何を一番叶えたいのかを先に聞く。

Scoring draft:

```csv
question_id,choice,primary_pole,secondary_pole
Q03,A,G,A
Q03,B,A,P
Q03,C,G,R
Q03,D,A,R
```
