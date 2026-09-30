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

## 評価対象: Plandex

- 形態: CLI
- リポジトリ: https://github.com/plandex-ai/plandex
- 運営メモ: 公式に Windows ビルドなし（darwin/linux/freebsd のみ）。WSL 必須のため本ベンチでは計測不可 — 導入可否の記録対象

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| L1 | localllm | — | — | — | 計測不能。Windows ビルドなし（WSL 必須）のため |
| L2 | localllm | — | — | — | 計測不能。Windows ビルドなし（WSL 必須）のため |
| L3 | localllm | — | — | — | 計測不能。Windows ビルドなし（WSL 必須）のため |

## 機能・環境面の調査メモ

- form: CLI
- os_windows: × Windowsビルドなし（WSL必須）
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ?
- local_llm: ○ OpenRouter等経由
- proxy_key_hiding: ?
- token_saving: ?
- telemetry: ?
- auto_approve: ?
- parallel: ?
- checkpoint: ?
- mcp: ?
- cost_display: ?
- account_required: △
- target_audience: 中級者
- 導入: × / WSL 必須 / 公式に Windows ビルドなし（darwin/linux/freebsd のみ）

以上のデータを踏まえて採点とコメントを返してください。