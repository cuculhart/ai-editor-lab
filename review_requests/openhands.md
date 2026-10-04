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

## 評価対象: OpenHands

- 形態: Web UI + Docker
- リポジトリ: https://github.com/All-Hands-AI/OpenHands
- 運営メモ: 自律エージェント型。CLI もあり

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | byok-gemini | ✓ | 32 | 0 | omise/discount.py を >= 3 に修正。accept.py: pass / tests未改変 / 全7テストpass（Agent Canvas版UIで実行）。run1は計測ミスのためrun2で再計測 |
| T2 | byok-gemini | ✓ | 80 | 0 | omise/points.py を新規追加（int(amount*0.01)で1%切り捨て）。accept.py: pass / 既存ファイル未改変 / 回帰なし |
| T3 | byok-gemini | ✓ | 86 | 0 | Cartをdict[(name,price)]管理にリファクタ。add/remove/count/quantities/subtotal全て公開API互換。accept.py: pass / cart suite pass（fixture由来のdiscount境界バグはT3範囲外で温存） |
| T4 | byok-gemini | ✓ | 29 | 0 | tests/test_cart.py 新規追加（3テスト: remove/quantities/混合product、全てpass）。accept.py: pass / 既存ファイル未改変（唯一の失敗はfixture由来のT1バグ） |
| T5 | byok-gemini | ✓ | 38 | 0 | README.md を初学者向けに全面改訂（概要/インストール/使い方+コード例/テスト実行/ライセンス全節あり・1569字）。accept.py: pass / 他ファイル未改変。※実行先が誤ってLocalLLM/T5 workspaceだったがBYOK(Gemini)実行のため byok-gemini に記録 |
| T6 | byok-gemini | ✓ | 25 | 0 | agent-canvas環境で再計測。静的・動的(playwright)検証とも全pass・介入0。run1(9/27・旧コンテナ・約15秒)も成功 |
| T1 | localllm | ✗ | 600+ | ? | 旧版: ctx 32768拡大済みでも litellm 300s タイムアウトを1ターンも完了できず中断（CPU推論で約30Kトークンのシステムプロンプト評価に10分超）。新版agent-canvasでも再検証: Ollama接続成功・timeout 1800sに延ばしたが推論中にOllamaプロセスが落ちてServerDisconnected。4B+CPUでは構造的に不成立 |
| T2 | localllm | ✗ | ? | 0 | 環境不成立のため未試行。T1で ctx 32768 拡大後も litellm 300s タイムアウト超過を確認（OpenHandsの巨大システムプロンプトが4B+CPUに不適合） |
| T3 | localllm | ✗ | ? | 0 | 環境不成立のため未試行。T1で ctx 32768 拡大後も litellm 300s タイムアウト超過を確認（OpenHandsの巨大システムプロンプトが4B+CPUに不適合） |
| T4 | localllm | ✗ | ? | 0 | 環境不成立のため未試行。T1で ctx 32768 拡大後も litellm 300s タイムアウト超過を確認（OpenHandsの巨大システムプロンプトが4B+CPUに不適合） |
| T5 | localllm | ✗ | ? | 0 | 環境不成立のため未試行。T1で ctx 32768 拡大後も litellm 300s タイムアウト超過を確認（OpenHandsの巨大システムプロンプトが4B+CPUに不適合） |

## 機能・環境面の調査メモ

- form: Webアプリ（Docker必須）
- os_windows: △ WSL2+Docker必須・winnat問題あり
- os_mac: ○
- os_linux: ○
- byok: ○ litellm形式で指定
- custom_endpoint: ○
- local_llm: ○ litellm経由
- proxy_key_hiding: △ litellm経由。モデル指定は litellm 形式 (gemini/...) が必要
- token_saving: ○ litellm経由のプロンプトキャッシュ（モデル依存）
- telemetry: △
- auto_approve: ○ 確認モード切替
- parallel: ○ 複数会話可
- checkpoint: △ サンドボックス内git管理
- mcp: ○
- cost_display: △ メトリクスあり
- account_required: 不要
- target_audience: 中〜上級者（Docker前提）
- 導入: △ / Docker Desktop（WSL2 必須） / Docker Desktop (WSL2) 必須。初回は winnat ポート除外問題で失敗→net stop/start winnat で解消。LLMプロファイルのベースURL欄に壊れたURLが自動入力され404エラーになる罠あり

以上のデータを踏まえて採点とコメントを返してください。