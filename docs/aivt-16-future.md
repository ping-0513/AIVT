# AIVT-16 Future Ideas

Status: future idea draft.

This file stores ideas that should be considered later for the AIVT-16 answer UI and response flow.

---

## Answer flow and persistence ideas

Raw idea notes:

- 全問回答してなくても送信可
- やってる途中とか読み込みなおしで消えるのをなくしたい
- でも途中で送信しようとするとこの問題が未回答ですがいいですか？ってなる
- 指定問題に戻れる、未回答問題に戻れる機能ほしい
- あと選択肢シャッフルで、選択肢IDは中で問題Ver1-Q1-Aみたいになってて、表向き（デフォルト）Aでも画面上Bとかに見えるような順番バイアスを低める仕組みつくりたい

---

## Draft requirements

### Partial submission

Users may submit responses even if some questions are unanswered.

Unanswered questions should be stored explicitly as unanswered.

### Draft persistence

Responses should not disappear while the user is answering.

Reloading the page should restore already selected answers.

### Submission confirmation

If the user attempts to submit with unanswered questions, the UI should show a confirmation before final submission.

The confirmation should indicate that some questions are unanswered and allow the user to either return to the unanswered questions or submit anyway.

### Navigation

The UI should allow users to return to a specific question.

The UI should also allow users to return to unanswered questions.

### Choice shuffling

Choice display order should be randomizable to reduce order bias.

Internal option IDs should remain stable even when visible labels change.

Example internal ID shape:

```text
AIVT-16-Ver1-Q1-A
```

Example behavior:

- Internal default option: `AIVT-16-Ver1-Q1-A`
- Visible label in one session: `B`

Scoring should use the internal option ID, not the visible label.

Saved responses should keep enough information to reconstruct what the user saw, including the selected internal option ID and visible display order.
