# Supabase・モデル選択メモ

Claude Codeに読ませるための実装注意メモ。

## Supabaseの注意

Supabaseからの通知によると、2026/05/30以降の新規プロジェクトでは、`public` schemaに作成した新規テーブルがData APIから自動で使えるとは限らない。

AIVTでSupabaseを使う場合は、新しいテーブルを作ったあと、Data APIから読める必要があるテーブルについて、roleごとの権限設定を明示する。

確認すること：

- questions / choices は公開表示に必要か
- results / result_answers はユーザー同意がある場合だけ保存するか
- admin_users は一般公開しない
- updates は公開表示してよいか
- RLSを有効にするか
- roleごとの読み取り・書き込み範囲が妥当か

PostgRESTで `42501` が出た場合は、コードだけでなくSupabase側の権限設定も確認する。

## Claude Codeでのモデル確認

Claude Codeを使う前に、今どのモデルで動いているか確認する。

Claude Opus 4.8は出たばかりなので、最初から全面実装を任せない。

確認すること：

- 使用中モデル
- Opus / Sonnet の違い
- effort設定
- Dynamic Workflowを使うかどうか
- 安全寄りの出力で設計判断が歪まないか
- 既存コードを壊さず読めるか

## Claude 4.8を使う場合

最初に任せてよいこと：

- READMEとdocsの読み込み
- MVP実装計画
- 変更予定ファイルの列挙
- 小さなUI部品の作成

最初に任せないこと：

- 全面実装
- DB設計の確定
- migration実行
- 認証設計の自動変更
- Dynamic Workflowでの大規模改修
- 自動commit / push

## Dynamic Workflow

Dynamic Workflowは強力そうだが、トークン消費が大きく、サブエージェントが並列に動くため、初手では使わない。

使う条件：

- git statusがclean
- 変更前commitがある
- README / docs / CLAUDE.mdを読ませた後
- スコープが狭い
- 実行前に計画を出す
- ユーザー承認後に実行する
