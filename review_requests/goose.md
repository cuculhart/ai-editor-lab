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

## 評価対象: Goose

- 形態: CLI + デスクトップ
- リポジトリ: https://github.com/block/goose
- 運営メモ: Block 製 OSS エージェント

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | byok-gemini | ✓ | 12 | 0 | pass |
| T2 | byok-gemini | ✓ | 24 | 0 | pass |
| T3 | byok-gemini | ✗ | 39 | 0 | 公開API維持を破壊：unhashable な @dataclass Product を dict キーに使用し TypeError。既存テストは通るが互換性シナリオで検出 |
| T4 | byok-gemini | ✓ | 16 | 0 | pass |
| T5 | byok-gemini | ✓ | 18 | 0 | pass |
| T6 | localllm | ✓ | ? | ? | ?。動的検証pass |
| T6 | byok-gemini | ✓ | 15 | 0 | 静的検証全pass・15秒。動的検証pass |
| L1 | localllm | ✗ | 900 | 0 | タイムアウト（15分上限）。ollama ps ではモデル処理中（CPU100%・コンテキスト32K）を確認するも初回応答が完了せず。巨大なシステムプロンプト＋ツールスキーマの評価がCPU推論で間に合わない。最小プロンプト(hi)でも85秒超無応答 |
| L2 | localllm | — | — | — | 計測不能。L1 で初回推論がタイムアウト内に完了しないため（システムプロンプト起因の決定的失敗） |
| L3 | localllm | — | — | — | 計測不能。L1 で初回推論がタイムアウト内に完了しないため（システムプロンプト起因の決定的失敗） |

## 機能・環境面の調査メモ

- form: CLI（+デスクトップアプリ）
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ○
- local_llm: ○ ollama
- proxy_key_hiding: ○
- token_saving: ?
- telemetry: △ opt-out可
- auto_approve: ○
- parallel: △
- checkpoint: △ セッションresume
- mcp: ○ extensions基盤
- cost_display: × 実測で表示なし
- account_required: 不要
- target_audience: 中級者
- 導入: ○ / zip 展開のみ / GitHub Releases の Windows zip

以上のデータを踏まえて採点とコメントを返してください。