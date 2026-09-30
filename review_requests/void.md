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

## 評価対象: Void

- 形態: VS Code フォーク
- リポジトリ: https://github.com/voideditor/void
- 運営メモ: OSS の Cursor 代替。独立エディタ

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T6 | byok-gemini | ✗ | 81 | 0 | プロジェクトフォルダ必須。空ファイル3つのみ生成（0バイト）。ツール呼び出しが10回以上エラーで破綻し、最終的にチャットへコード出力→ユーザーコピペ要求。しかも出力コードは要件外（id="start-btn"・class="hole"）。81秒 |
| L1 | localllm | ✓ | ? | 1 | calc.py作成(sorted+filterで仕様完全一致・検証済)。ファイル生成のみなら完走可能 |
| L2 | localllm | ✗ | ? | 2 | 編集は適用されたが行頭インデントを喪失しIndentationError(ファイル破壊)。完了宣言あり・実行結果は更に悪化 |
| L3 | localllm | ✓ | ? | 4 | 自力デバッグで原因特定→EDITは2回失敗後3回目で成功→unittestで全7件合格を自己確認(検証済)。PowerShellで&&不可のエラー1回 |

## 機能・環境面の調査メモ

- form: スタンドアロンIDE（VS Codeフォーク）
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ○
- local_llm: ○ Ollama対応を標榜
- proxy_key_hiding: ○ プロバイダ直接接続
- token_saving: ?
- telemetry: ○ プライバシー重視設計
- auto_approve: △ gemini-3.5-liteでツール呼出し破綻
- parallel: ?
- checkpoint: ○
- mcp: ○
- cost_display: ?
- account_required: 不要（プロジェクトフォルダ必須）
- target_audience: 中級者
- 導入: ○ / zip ポータブル / Void.exe 展開して起動。インストーラ不要

以上のデータを踏まえて採点とコメントを返してください。