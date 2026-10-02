# ベンチマーク実施状況

生成: 2026-10-01 13:15 +0900 — `tools/status.py` により自動生成

再生成: `python tools/status.py`（`results/`・`reviews/`・`runs/` 更新後に実行）

記号: `✓` 成功 / `✗` 失敗 / `?` 枠あり・未計測 / `—` 枠なしまたは省略（計測不可）。
同一タスク複数runは `✓(n/m)` の形式。成果物ありだが結果未記録は「乖離」節を参照。

## サマリ

| カテゴリ | モデル | ✓ | ✗ | ? | — |
|---|---|---|---|---|---|
| BYOK（Gemini系） | gemini-3.5-flash-lite | 28 | 5 | 36 | 0 |
| LocalLLM系 | qwen3.5:4b (Ollama) | 20 | 13 | 4 | 17 |
| その他系 | — | 0 | 1 | 0 | 0 |

## 定量ベンチ 実施状況（ツール×タスク）

### BYOK（Gemini系）（gemini-3.5-flash-lite）

| ツール | T1 | T2 | T3 | T4 | T5 | T6 |
|---|---|---|---|---|---|---|
| Cline | ? | ? | ? | ? | ? | ✓(2/2) |
| Zoo Code | ? | ? | ? | ? | ? | ✓ |
| Kilo Code | ? | ? | ? | ? | ? | ✓ |
| Continue | ? | ? | ? | ? | ? | ✓(1/2) |
| OpenHands | ? | ? | ? | ? | ? | ✓ |
| SWE-agent | — | — | — | — | — | ✗ |
| OpenCode | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Aider | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Goose | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Plandex | ? | ? | ? | ? | ? | ? |
| Void | ? | ? | ? | ? | ? | ✗ |
| Teaspoon IDE | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ |

### その他系

| ツール | T6 |
|---|---|
| Roo Code | ✗ |

### LocalLLM系（qwen3.5:4b (Ollama)）

| ツール | L1 | L2 | L3 | T1 | T2 | T3 | T4 | T5 | T6 |
|---|---|---|---|---|---|---|---|---|---|
| Cline | ✓ | ✓ | ✓ | — | — | — | — | — | ✓ |
| Roo Code | ✗ | — | — | — | — | — | — | — | — |
| Zoo Code | ✗ | — | — | — | — | — | — | — | ✓ |
| Kilo Code | — | — | — | — | — | — | — | — | ✓ |
| Continue | ✗ | ✗ | ✗ | — | — | — | — | — | ✓ |
| OpenHands | ? | ? | ? | — | — | — | — | — | ✓ |
| Devika | — | — | — | — | — | — | — | — | — |
| OpenCode | ✗ | — | — | — | — | — | — | — | ✓ |
| Aider | ✗ | ✓ | ✗ | — | — | — | — | — | ✓ |
| Goose | ✗ | — | — | — | — | — | — | — | ✓ |
| Plandex | — | — | — | — | — | — | — | — | — |
| Void | ✓ | ✗ | ✓ | — | — | — | — | — | ? |
| Teaspoon IDE | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ | ✓ |

## 定性評価・レビュー記入状況

| ツール | 機能マトリクス | 導入の容易さ | ChatGPT | Gemini | Claude | Devin (SWE-2) |
|---|---|---|---|---|---|---|
| Cline | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Roo Code | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Zoo Code | △16/17 (16/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Kilo Code | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Continue | ✓ (18/18) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| OpenHands | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Devika | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| SWE-agent | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| OpenCode | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Aider | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Goose | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Plandex | △16/17 (16/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Void | △16/17 (16/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |
| Teaspoon IDE | ✓ (17/17) | △3/6 (3/6) | ✓ | ✓ | ✓ | ✓ |

## runs/ 成果物と results/ の照合

### 成果物あり・results 未記録（記録漏れの可能性）

- `runs/sweagent/T1/` (1 run) — results に行なし

### results に成功記録・成果物なし

- aider T6 run1: 成功だが diff_url 未採取
- cline T6 run1: 成功だが diff_url 未採取
- continue T6 run1: 成功だが diff_url 未採取
- forger T6 run1: 成功だが diff_url 未採取
- goose T6 run1: 成功だが diff_url 未採取
- kilocode T6 run1: 成功だが diff_url 未採取
- opencode T6 run1: 成功だが diff_url 未採取
- openhands T6 run1: 成功だが diff_url 未採取
- zoocode T6 run1: 成功だが diff_url 未採取

## 残作業の目安

- Cline: 未計測 5 枠
- Zoo Code: 未計測 5 枠
- Kilo Code: 未計測 5 枠
- Continue: 未計測 5 枠
- OpenHands: 未計測 8 枠
- Plandex: 未計測 6 枠
- Void: 未計測 6 枠
