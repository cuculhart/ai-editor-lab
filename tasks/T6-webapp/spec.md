# T6: Webアプリ生成（モグラ叩き）

## 内容

ゼロから 3 ファイル構成のブラウザゲームを生成させるメインタスク。
オセロより単純だが、DOM 生成・イベント・タイマー・ランダム性・状態遷移を含むため、
低性能モデルでのツール差（構成力・要求の取りこぼし）が出やすい。

Gemini 3.5 Flash-Lite 固定の BYOK 系計測における基準プロンプト。
GUI ツール（VS Code 拡張系）の手動評価もこのプロンプトを投げるだけでよい設計。

## 検証方法（accept.py）

静的チェック（常時）:
1. index.html / style.css / script.js の3ファイルが存在
2. index.html が style.css と script.js を読み込んでいる
3. 指定要素 id="start-button" / id="score" / id="timer" が存在
4. 外部 CDN/ライブラリの読み込みがない
5. script.js にイベントハンドラ相当の記述がある

動的チェック（playwright が使える環境のみ・任意）:
- ページを開き #start-button クリック → 一定時間内に .mole が出現
- .mole クリックで #score が増加することを確認
