# AIコーディングツール評価の依頼

あなたは「初学者向けAIコーディングツール比較サイト」のレビュアーです。
以下のベンチマーク実測データを読み、このツールを **初学者が使う場合の観点** で
8つの軸について 0〜5 の整数で採点し、短いコメントを添えてください。

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
- overall: 総合評価（初学者におすすめできるか）

## 回答フォーマット

以下のJSONのみを返してください（```json フェンス不要・そのまま貼り付けられる形）:

{
  "scores": {
    "audience": 0, "ui": 0, "learning": 0, "steering": 0,
    "stuck_free": 0, "error_handling": 0, "speed_feel": 0, "overall": 0
  },
  "comment": "（2〜3文の日本語コメント）"
}

---

## 評価対象: Kilo Code

- 形態: VS Code 拡張
- リポジトリ: https://github.com/Kilo-Org/kilocode
- 運営メモ: Roo Code 系フォーク。ユーザー数大 LocalLLM計測はL1で全システムフリーズ(強制電源断)により断念

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T6 | localllm | ✓ | ? | ? | ?。動的検証pass |
| T6 | byok-gemini | ✓ | 42 | 5 | 静的検証全pass・42秒・6 steps。動的検証pass |
| L1 | localllm | — | — | — | 計測断念。実行中に応答待ちが5分超続いた後PCが完全フリーズ(ブラックアウト・Ctrl+Alt+Del無効)し強制電源断。Event41のみ・BugCheckなし=OS応答不能。一般的ビジネスPCでは実用不能と判断 |
| L2 | localllm | — | — | — | 計測断念。L1で全システムフリーズのため以降は実施せず |
| L3 | localllm | — | — | — | 計測断念。L1で全システムフリーズのため以降は実施せず |

## 機能・環境面の調査メモ

- form: VS Code 拡張（Roo系フォーク）
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ○
- local_llm: ○ Ollama等
- proxy_key_hiding: △ モデル選択肢のデフォルトがKilo gateway経由（透かし表示）で、BYOKには自分でGoogleプロバイダ選択が必要
- token_saving: ○ キャッシュ実測 hit 69.5%
- telemetry: ?
- auto_approve: ○
- parallel: ?
- checkpoint: ○
- mcp: ○
- cost_display: ○ in/out/reasoning/cache の詳細内訳
- account_required: △ BYOKなら不要（gateway選択時は要Kiloアカウント）
- target_audience: 初学者〜中級者
- 導入: ○ / VS Code 拡張 / Marketplace から通常導入。初回のモデル選択で Kilo アカウントログイン画面 (app.kilo.ai) に誘導される

以上のデータを踏まえて採点とコメントを返してください。