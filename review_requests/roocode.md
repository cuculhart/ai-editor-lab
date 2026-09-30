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

## 評価対象: Roo Code

- 形態: VS Code 拡張
- リポジトリ: https://github.com/RooCodeInc/Roo-Code
- 運営メモ: v3.54.0 で開発終了・リポアーカイブ済み（2026-05-15）。後継 Roomote はクラウドエージェント製品でIDEツールではないため対象外。コミュニティ継続は Zoo Code 系へ。計測試行は Gemini・Ollama 両経路で無応答（バックエンド停止の可能性）→ 評価不能として記録

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T6 | other | ✗ | ? | ? | 計測不能。両モデルで「APIリクエスト...」のまま2分以上無応答。タイムアウト・エラー表示なし。開発終了済みのためバックエンド側が死んでいる可能性 |
| L1 | localllm | ✗ | 180 | ? | 計測不能。「こんにちは」にも3分以上無応答（CPU100%推移で終了）。ollama再起動+BaseURL明示後もローカルLLMへのアクセス自体が発生せずハング。Gemini・Ollama両経路で不動 |
| L2 | localllm | — | — | — | 計測不能。L1 でローカルLLMへのリクエスト自体が発生せず応答不能のため |
| L3 | localllm | — | — | — | 計測不能。L1 でローカルLLMへのリクエスト自体が発生せず応答不能のため |

## 機能・環境面の調査メモ

- form: VS Code 拡張（開発終了）
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: △ 設定上は可能だが実際に API が応答せず
- custom_endpoint: ?
- local_llm: ?
- proxy_key_hiding: ?
- token_saving: ?
- telemetry: △ 収集あり
- auto_approve: ○ 設定あり
- parallel: ?
- checkpoint: ○
- mcp: ○
- cost_display: ?
- account_required: 不要
- target_audience: 非推奨（2026-05 開発終了・API無応答）
- 導入: △ / VS Code 拡張 / Marketplace最終版 v3.54.0。gemini-3.5-flash-lite 非対応。別モデルでも API リクエスト無応答で実使用不能

以上のデータを踏まえて採点とコメントを返してください。