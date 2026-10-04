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

## 評価対象: SWE-agent

- 形態: CLI（Docker バックエンド）
- リポジトリ: https://github.com/SWE-agent/SWE-agent
- 運営メモ: SWE-bench チーム製の自律エージェント。sweagent run で駆動。Docker サンドボックス前提。T6 失敗後、現バージョン(v1.1.0)は Windows 標準 clone(autocrlf) で submit 不能と判明し以降の計測を見送り — 評価不能として記録

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T6 | byok-gemini | ✗ | 320 | 0 | Docker コンテナ内で3ファイル生成まで到達したが、ステップ上限（23 API calls）で submit せず終了。自己検証用テスト（test_game.py）作成に多数ステップを消費。トークン消費は他ツールの数倍 |

## 機能・環境面の調査メモ

- form: CLIエージェント（Docker sandbox）
- os_windows: △ Docker必須・cp932回避(PYTHONUTF8)・空リポ不可・autocrlf環境のcloneでsubmit不可（ツールスクリプトCRLF化）
- os_mac: ○
- os_linux: ○
- byok: ○ litellm
- custom_endpoint: ○
- local_llm: △ tool calling要検証
- proxy_key_hiding: ○
- token_saving: △ 実測で過剰消費
- telemetry: ○ 収集機能なし
- auto_approve: ○ 全自動
- parallel: ×
- checkpoint: ×
- mcp: ×
- cost_display: ○ trajに記録
- account_required: 不要
- target_audience: 研究者・上級者
- 導入: △ / Docker + Python 3.12 / PyPI 非対応。ソースインストール要・Windows は PYTHONUTF8=1 必須＋パス長問題あり＋git clone は core.autocrlf=false で（CRLF化するとコンテナ内 submit が恒久的に失敗）

以上のデータを踏まえて採点とコメントを返してください。