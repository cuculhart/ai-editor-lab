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

## 評価対象: Teaspoon IDE

- 形態: 独立 Electron アプリ
- リポジトリ: https://github.com/cuculhart/teaspoon-ide
- 運営メモ: エクスプローラー/Monaco/Git/TTY一体型。旧称 Forger

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T1 | byok-gemini | ✓ | 20 | 4 | 正解修正(quantity>=3)を適用し外部検証で全7テスト合格。承認4回。Playwright/CDP自動化 |
| T2 | byok-gemini | ✓ | 20 | 4 | omise/points.pyにearn_pointsを正しく実装。既存テスト末尾にTestPointsクラスを追記（既存メソッドの改変なし）。ベースライン既知バグのみ残存 |
| T3 | byok-gemini | ✗ | 37 | 10 | 公開関数apply_bulk_discount(product_price,quantity)を(subtotal,quantity)に意味変更しtest_apply_bulk_discount破壊。Cart.remove()を1個削除→全個削除に意味変更。Productをfrozen化。振る舞い維持要件に違反 |
| T3 | byok-gemini | ✗ | ? | 5 | v0.7.0で3度目の手動実行。remove()の1個削除意味論・公開API互換を維持しaccept pass。内部はlist+Counter(quantities)構成（ZooCodeと同型）。run1/run2はremove全削除・シグネチャ変更で失敗 【訂正】強化版accept.py(real_refactor判定)ではcart.pyがベースラインとバイト同一=no-opのため不合格。旧acceptはAPI互換+テストのみでno-opを検出できなかった |
| T3 | byok-gemini | ✗ | ? | 4 | 実際にdict[tuple]+_CartItemへリファクタしたが、存在しないProduct.categoryを参照してAttributeError・全テスト落ち。テスト失敗(fixture由来のT1バグ)を環境破壊と誤診しPATH/hostedtoolcacheを探索する空転が約30ステップ。1回目の回答は編集前に「全テストパス」と虚偽報告しnudgeで継続 |
| T4 | byok-gemini | ✓ | 12 | 2 | tests/test_cart.py新規作成（3メソッド: remove・混在quantities・未存在remove例外）。既存ファイル不変、追加テスト全合格 |
| T5 | byok-gemini | ✓ | 12 | 1 | README.mdのみ変更。概要・インストール・使い方(コード例付)・テスト実行・ライセンスの全必須節を満たす |
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
| T3 | byok-gemini | ✗ | ? | 3 | EDIT_FILEがSEARCH不一致で失敗後、編集を再試行せずTestCartのみ実行(exit 0)して完了報告。cart.pyはfixtureとバイト同一=no-op+虚偽報告。exit0のコマンドが編集失敗フラグを上書きクリアするバグを露呈(unresolvedEdit分離で修正済み)。環境探査ループは改善版で消失 |
| T3 | byok-gemini | ✓ | ? | 5 | unresolvedEdit分離+コマンド結果分類ヒント版。真のdict化(list[Product]→dict[(name,price)])を実施しaccept pass。環境探査ゼロ、最終回答はTestCart passのみを正確に報告(全体suiteのfixture由来失敗を虚偽せず)。run5のno-op虚偽報告はunresolvedEditで防止 |
| T3 | byok-gemini | ✗ | ? | 4 | dict[Product,int]設計だがProductは非frozen dataclassでunhashable→TypeError。quantities()もdict[Product,int]返却で公開APIの意味(商品名→数)を破壊。検証不足 |
| T3 | byok-gemini | ✓ | ? | 3 | dict[(name,price)]→_CartEntry dataclassへの真のリファクタでaccept pass。ロールバック機能でfixture復元してからの再実行。介入3は最小記録 |
| T3 | byok-gemini | ✗ | ? | 1 | no-op: cart.pyがベースラインとバイト同一(run5と同型・編集せず完了報告と推測)。強化版acceptのreal_refactorで検出 |
| T3 | byok-gemini | ✓ | ? | 3 | dict[tuple[str,int]]化でaccept pass。途中EDIT失敗→dict[Product]虚偽報告→hash不可を自力で検出→2度目のeditでtuple keyに修正し回復。完了宣言時は編集成功済みのため警告非表示（仕様通り） |
| T3 | byok-gemini | ✗ | ? | 4 | dict[Product,int]でunhashable踏破(run7と同型)。hash(p)を2回実行してexit1を確認した直後に同設計を書く矛盾行動。TestCart exit1の直後に「全テストパス」と虚偽報告 |

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