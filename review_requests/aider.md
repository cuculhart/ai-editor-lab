# AIコーディングツール評価の依頼

あなたは「初学者向けAIコーディングツール比較サイト」のレビュアーです。
以下のベンチマーク実測データを読み、このツールを **初学者が使う場合の観点** で
9つの軸について 0〜5 の整数で採点し、短いコメントを添えてください。

## 評価の前提

- 読者はプログラミング初学者・AIツール初心者
- 「難しい設定なしに動くか」「弱いモデルでもちゃんと動くか」が主要な評価軸
- データに無い項目は憶測で書かず、データから読み取れる範囲で評価する
- コメントは日本語で2〜3文、具体的な根拠（実測値・失敗形）に言及する

## ベンチマークの内容（共通）

- **fixture**: 小さなPythonパッケージ(omise)。意図的に1件の失敗テスト
  （割引境界値 `quantity > 3` → 正しくは `>= 3`）を含む
- **T系タスク**: T1バグ修正/T2機能追加/T3リファクタ/T4テスト生成/T5ドキュメント/T6静的Webアプリ生成
- **L系タスク（ローカルLLM向け）**: L1新規ファイル作成/L2誘導付き1行修正/L3自力デバッグ
- **モデル**: BYOK系=gemini-3.5-flash-lite、LocalLLM系=Ollama qwen3.5:4b（CPU推論）
- **環境**: Windows 11 + Ryzen 5 4500U（CPU内蔵GPU）+ 32GB の一般的ミニPC
- **上限**: 1タスク15分。介入=承認クリックや手修正指示の回数
- 記号: ✓成功 ✗失敗 — 計測断念/不能（理由はnotesに記載）

## 採点軸（0〜5）

- audience: ターゲット層の明確さ
- ui: 画面の見やすさ
- learning: 学習コスト（低いほど高得点）
- steering: エージェントの操縦性（指示通りに動くか）
- stuck_free: 詰まりにくさ
- error_handling: エラー時の挙動（自己回復・説明力）
- speed_feel: 体感速度
- security: 安心して使えるか（テレメトリー有無・opt-out可否、BYOKでもベンダーサーバーへ
  データが流れる設計がないか、プロキシでのキー隠蔽可否、アカウント要否、
  非操作中に動く機能［自動補完等］の外部通信、ハング中の課金継続の有無）
- overall: 総合評価（初学者におすすめできるか）

## 回答フォーマット

以下のJSONのみを返してください（```json フェンス不要・そのまま貼り付けられる形）:

{
  "scores": {
    "audience": 0, "ui": 0, "learning": 0, "steering": 0,
    "stuck_free": 0, "error_handling": 0, "speed_feel": 0, "security": 0,
    "overall": 0
  },
  "comment": "（2〜3文の日本語コメント）"
}

---

## 評価対象: Aider

- 形態: CLI
- リポジトリ: https://github.com/Aider-AI/aider
- 運営メモ: CLI の代表格。--yes で自動化しやすい

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | byok-gemini | ✓ | 21 | 0 | git環境で全pass。初回 --no-git では repo-map 無効でファイル未発見→git init 後に再計測 |
| T2 | byok-gemini | ✓ | 11 | 0 | git環境で全pass。初回 --no-git では repo-map 無効でファイル未発見→git init 後に再計測 |
| T3 | byok-gemini | ✓ | 20 | 0 | git環境で全pass。初回 --no-git では repo-map 無効でファイル未発見→git init 後に再計測 |
| T4 | byok-gemini | ✓ | 13 | 0 | git環境で全pass。初回 --no-git では repo-map 無効でファイル未発見→git init 後に再計測 |
| T5 | byok-gemini | ✓ | 13 | 0 | git環境で全pass。初回 --no-git では repo-map 無効でファイル未発見→git init 後に再計測 |
| T6 | localllm | ✓ | ? | ? | ?。動的検証pass（opacity制御の実装、安定して得点確認） |
| T6 | byok-gemini | ✓ | 17 | 0 | 静的検証全pass・17秒・単発メッセージで完結（--yes-always --exit --no-fancy-input）。動的検証pass（opacity制御の実装、安定して得点確認） |
| L1 | localllm | ✗ | 420 | 0 | 偶数フィルタは実装したが「昇順」の要件を落とした（sorted なし）。CPU環境で7分 |
| L2 | localllm | ✓ | 120 | 0 | 誘導付きなら正確に1行修正（編集適用まで約2分）。ただし編集完了後にaiderプロセスが応答なくハングし手動kill |
| L3 | localllm | ✗ | 622 | 0 | UTF-8ファイルをcp932で読み文字化け→docstringを「構文エラー」と誤診し models.py/checkout.py を実質同一内容で上書き。本物のバグ(discount.py)には未着手。テストも未実行 |

## 機能・環境面の調査メモ

- form: CLI
- os_windows: △ --no-fancy-input必須・git前提
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ○ litellm
- local_llm: ○ ollama
- proxy_key_hiding: ○ litellm経由
- token_saving: ○ repo-map・cache prompts
- telemetry: △ analytics・opt-out可
- auto_approve: ○ --yes-always
- parallel: ×
- checkpoint: ○ git commit/undo
- mcp: ×
- cost_display: ○ message/session毎
- account_required: 不要
- target_audience: 中級者（git前提）
- 導入: △ / Python / Python 3.14 では依存ビルド不可 → uv で 3.12 環境に導入

以上のデータを踏まえて採点とコメントを返してください。