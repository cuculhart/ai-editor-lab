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

## 評価対象: Teaspoon IDE

- 形態: 独立 Electron アプリ
- リポジトリ: https://github.com/cuculhart/teaspoon-ide
- 運営メモ: エクスプローラー/Monaco/Git/TTY一体型。旧称 Forger

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | localllm | ✓ | 901 | 3 | 正解修正(quantity>=3)を適用し外部検証で全7テスト合格。修正後の自己検証ループで空転し完了応答前に900秒上限。Playwright/CDP自動化、CORS対策のlocalhostプロキシ経由 |
| T2 | localllm | ✗ | 902 | 0 | タイムアウト。EDITブロックのSEARCH/REPLACE構文を繰り返し誤生成し、承認可能な編集に至らず |
| T3 | localllm | ✗ | 901 | 0 | タイムアウト。EDIT構文誤生成(no SEARCH/REPLACE blocks found)を繰り返し編集未適用 |
| T4 | localllm | ✗ | 501 | 1 | tests/test_cart.py新規追加・自然完了したが、追加テスト自身が失敗(removeが1個のみ削除の仕様を全削除と誤認) |
| T5 | localllm | ✓ | 712 | 1 | 必須5節すべて含み他ファイル未変更。ただしコード例は実APIと異なる創作APIを記述(質は限定的) |
| T6 | localllm | ✓ | ? | ? | ?。動的検証pass |
| T6 | byok-gemini | ✓ | 10 | 2 | 静的検証全pass・10秒・全ツール中最速。動的検証pass |
| L1 | localllm | ✓ | 283 | 1 | 昇順ソート含め全要件pass。応答開始2分・完了4分43秒。軽量コンテキスト設計がCPU環境で有効 |
| L2 | localllm | ✓ | 298 | 1 | 誘導付きバグ修正を完遂。READ→EDIT→報告の3ステップで計298秒。メモリ使用率47%。Teaspoon IDEはファイル更新に承認必須の安全設計（介入1=編集承認） |
| L3 | localllm | ✓ | 740 | 3 | 誘導なしで完遂：自らpytest実行→失敗テスト特定→原因読解→修正。pip install pytestも自力。計740秒（7ステップ） |

## 機能・環境面の調査メモ

- form: スタンドアロンIDE
- os_windows: ○
- os_mac: ○ Git clone + npm run dev
- os_linux: ○ deb提供（またはGit clone + npm run dev）
- byok: ○
- custom_endpoint: ○ LLM_PROXY_URL でLiteLLMプロキシ指定可
- local_llm: ○ Ollama対応
- proxy_key_hiding: ○ プロキシ側に本物のキーを置ける
- token_saving: ◎ ファイルツリー優先送信＋オンデマンド取得で大幅削減（Context optimization）
- telemetry: ◎ テレメトリー自体が存在しない
- auto_approve: ○
- parallel: ×
- checkpoint: ○
- mcp: × 独自プロトコル
- cost_display: △ 非組織モードでは非表示
- account_required: 不要（ソロ）
- target_audience: 初学者〜中級者
- 導入: ○ / 単一 exe / 配布 zip/exe

以上のデータを踏まえて採点とコメントを返してください。