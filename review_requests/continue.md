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

## 評価対象: Continue

- 形態: VS Code/JetBrains 拡張
- リポジトリ: https://github.com/continuedev/continue
- 運営メモ: チャット型だがエージェントモードあり

## 定量ベンチ結果

| タスク | カテゴリ | 成否 | 秒 | 介入 | notes |
|---|---|---|---|---|---|
| T6 | localllm | ✓ | ? | ? | ?。生成3ファイルは動的検証pass。ただし生成完了応答でハング |
| T6 | byok-gemini | ✓ | ? | ? | 3ファイル生成後ハング（成果物自体は静的検証pass）。生成3ファイルは動的検証pass。ただし生成完了応答でハング |
| T6 | byok-gemini | ✗ | >300 | 2 | index.html・style.css 生成後、script.js 生成中に 'Generating...' 表示のまま5分以上ハング→手動キャンセル。script.js 未生成でハング |
| L1 | localllm | ✗ | ? | 1 | 2分以内にcalc.py作成・介入1。ただし昇順ソート未実装で例と不一致(even_numbers([3,1,4,2])が[4,2]を返す)→仕様未達 |
| L2 | localllm | ✗ | ? | ? | 約4分で応答終了したが編集は一切未適用・完了宣言なし。capabilities:tool_use有効化+Agentモードで再試行しても同じく編集なし → qwen3.5:4bがContinueのツール呼び出しを発行しないと判断 |
| L3 | localllm | ✗ | ? | 1 | Pythonプロジェクトにnpm testを誤実行(ENOENT)→ls提案で停止・編集なし。tool_use有効でもツール呼び出しが機能せず終了 |

## 機能・環境面の調査メモ

- form: VS Code / JetBrains 拡張
- os_windows: ○
- os_mac: ○
- os_linux: ○
- byok: ○ config.yaml
- custom_endpoint: ○
- local_llm: ○ Ollama定番
- proxy_key_hiding: ○
- token_saving: ?
- telemetry: △ 匿名収集・opt-out可
- auto_approve: △ ポリシー設定
- parallel: ?
- checkpoint: ○
- mcp: ○
- cost_display: × 表示なし
- account_required: △ Hub利用時のみ要（BYOKはローカル設定可）
- target_audience: 中級者（config.yaml編集前提）
- session_persist: △ gemini-3.5-flash-lite で2回連続ハング（生成途中・生成完了直後）
- 導入: ○ / VS Code 拡張 / Marketplace から通常導入

以上のデータを踏まえて採点とコメントを返してください。