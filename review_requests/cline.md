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

## 評価対象: Cline

- 形態: VS Code 拡張
- リポジトリ: https://github.com/cline/cline
- 運営メモ: 人気最大級。BYOK・Ollama 対応

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | byok-gemini | ✓ | ? | 3 | omise/discount.py を >= 3 に修正。accept.py: pass / tests未改変 / 全テストpass |
| T2 | byok-gemini | ✓ | ? | 5 | omise/points.py 追加（math.floor(amount*0.01)）＋任意のtests/test_points.pyも生成。accept.py: pass / 回帰なし |
| T3 | byok-gemini | ✓ | ? | 10 | Cartをdict[Product,int](defaultdict)管理にリファクタ。公開API互換・remove意味論正確。accept.py: pass / cart suite pass |
| T4 | byok-gemini | ✓ | ? | 6 | tests/test_cart.py 新規追加（3テスト: remove/quantities/混合product、全てpass）。accept.py: pass / 既存ファイル未改変 |
| T5 | byok-gemini | ✓ | ? | 5 | README.md全面改訂（全必須節・コード例あり）。accept.py: pass。ただし「他のファイルは変更しない」の指示に反して omise/discount.py のバグ(> 3→>= 3)も修正した点は注意 |
| T6 | localllm | ✓ | ? | ? | ?。動的検証pass |
| T6 | byok-gemini | ✓ | <60 | 4 | 静的検証全pass・1分未満。動的検証pass |
| T6 | byok-gemini | ✓ | 30 | 0 | 静的検証全pass・30秒・$0.0091。動的検証 3回中2回pass（モグラ表示600-1200msで自動クリックが不安定） |
| L1 | localllm | ✓ | ? | 2 | 1回目はパスタイポ(eijarai)＋write_to_file未使用でシェル力技→失敗。ユーザがパスを明示後に成功。介入2＝パス誘導＋mkdir承認。ただし calc/ サブディレクトリを余分に作成し「1ファイルのみ」の要件から逸脱 |
| L2 | localllm | ✓ | ? | 0 | 誘導付き1行修正を完走・全7テスト合格(検証済)。トークンは報告値の順序通り |
| L3 | localllm | ✓ | ? | 5 | 自力デバッグ完走・全7テスト合格(検証済)。初回編集はテキスト不一致で失敗→typeコマンドで再確認(文字化け)後に再編集して成功。PowerShellで&&非対応のエラーも1回 |
| T1 | localllm | ✓ | ? | 3 | discount.pyのquantity>3を>=3に修正・全7テスト合格(accept.py検証済)。初手でcmd系(dir /b, findstr)をPowerShellに投げて失敗、存在しないテストファイル名(test_speech.py等)を読もうとするハルシネーションの後に実ファイルを特定して一発修正 |
| T2 | localllm | ✗ | ? | 17 | 介入17・永久リトライで中断。earn_pointsのロジック自体は正しいがpoints.pyにリテラル\"\"\"混入でSyntaxError、さらに__init__.pyをPowerShellの>リダイレクトでUTF-16化しnullバイト混入→パッケージimportでコレクションエラー・既存テスト全滅。シェル統合が応答を返さずコマンド成功を確認できない状態に陥りOllama 300sタイムアウト2回 |
| T3 | localllm | ✗ | ? | 7 | 介入7で打ち切り。write_to_fileが機能せずシェル迂回を試みるも、JSON配列形式の疑似コードをPowerShellにそのまま投入→パースエラーの泥沼。cart.py本体は無傷だがcart.py.bak/cart_backup.pyの残骸あり。書こうとしていた実装はsubtotal()で数量を価格として渡す意味論バグを含んでおり、仮に書き込み成功でもaccept不合格だった |
| T4 | localllm | ✗ | ? | 8 | write_to_fileは機能しtests/test_cart.pyに7メソッド追加(要件3件超過)。ただしtest_remove_mixed_productsがremove「1個削除」の仕様を「全削除」と誤認し1件失敗→修復中にPowerShell表示の文字化け(CP932)をファイル破壊と誤診、chardet未導入で確認も失敗→Ollama BodyTimeoutErrorで終了。ファイル自体はUTF-8で無傷、あと一歩だった |
| T5 | localllm | ✓ | ? | 0 | 介入0で完走。README.mdを2回のeditで5節(概要/インストール/使い方[コード例付]/テスト実行/ライセンス)すべて充足・他ファイル無改変(accept.py検証済)。読み取り→編集→再確認の素直な手順で迷走なし |

## 機能・環境面の調査メモ

- form: VS Code 拡張
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: ○
- custom_endpoint: ○
- local_llm: ○ Ollama等
- proxy_key_hiding: ○ LiteLLM/OpenAI互換経由可
- token_saving: ○ プロンプトキャッシュ対応
- telemetry: △ 収集あり・opt-out可
- auto_approve: ○ 設定で介入0可
- parallel: △ 単一タスク主体
- checkpoint: ○
- mcp: ○
- cost_display: ○ タスク毎に表示
- account_required: 不要
- target_audience: 初学者〜中級者
- 導入: ○ / VS Code 拡張 / Marketplace から通常導入

以上のデータを踏まえて採点とコメントを返してください。