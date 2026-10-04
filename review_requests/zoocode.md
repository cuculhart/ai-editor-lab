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

## 評価対象: Zoo Code

- 形態: VS Code 拡張 + CLI
- リポジトリ: https://github.com/Zoo-Code-Org/Zoo-Code
- 運営メモ: Roo Code のコミュニティフォーク。CLI 実行可

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | byok-gemini | ✓ | ? | 7 | omise/discount.py を >= 3 に修正。accept.py: pass / tests未改変 / 全テストpass |
| T2 | byok-gemini | ✓ | ? | 10 | omise/points.py 追加（math.floor(amount*0.01)）。accept.py: pass / 回帰なし |
| T3 | byok-gemini | ✗ | ? | 16 | Cartを内部Counter併用のlist管理にリファクタ（公開API互換）。accept.py: pass / cart suite pass 【訂正】強化版accept.py(real_refactor判定)ではcart.pyがベースラインとバイト同一=no-opのため不合格。API互換・TestCart passは事実だが実質リファクタなし |
| T4 | byok-gemini | ✓ | ? | 6 | tests/test_cart.py 新規追加（3テスト、全てpass）。accept.py: pass / 既存ファイル未改変 |
| T5 | byok-gemini | ✓ | ? | 5 | README.md全面改訂（全必須節・コード例あり・1312字）。accept.py: pass / 他ファイル未改変 |
| T6 | localllm | ✓ | ? | ? | ?。動的検証pass |
| T6 | byok-gemini | ✓ | 60 | 7 | 静的検証全pass・約1分弱。動的検証pass |
| L1 | localllm | ✗ | ? | ? | 実用不能。localhost指定はfetch failed（127.0.0.1で接続確立）。qwen3.5:4bは思考ON/OFF両方でfetch failed（ロードtimeout推定）。qwen2.5-coder:1.5bは応答するも、ツール呼出しをJSONテキストとして出力・無関係な質問を幻覚（「こんにちは」にfrontend-config.jsonの所在を尋ねる） |
| L2 | localllm | — | — | — | 計測不能。L1 でローカルLLM接続・tool calling が実用不能のため実行不可 |
| L3 | localllm | — | — | — | 計測不能。L1 でローカルLLM接続・tool calling が実用不能のため実行不可 |

## 機能・環境面の調査メモ

- form: VS Code 拡張（Roo系フォーク）
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ○
- local_llm: ○ Ollama等
- proxy_key_hiding: ○
- token_saving: ○ コンテキスト使用量表示
- telemetry: ?
- auto_approve: ○
- parallel: △ 単一タスク主体
- checkpoint: ○
- mcp: ○
- cost_display: ○
- account_required: 不要
- target_audience: 初学者〜中級者
- 導入: ○ / VS Code 拡張 / Marketplace から通常導入

以上のデータを踏まえて採点とコメントを返してください。