# T2: 機能追加

## 内容

新規モジュール `omise/points.py` に `earn_points(amount: int) -> int` を実装させる。
「税抜き金額の1%、小数切り捨て」という明確な小仕様を、仕様記述だけから実装できるかを見る。

## 検証方法（accept.py）

1. `omise/points.py` が存在し `earn_points` が正しい値を返す（1000→10, 150→1, 99→0, 0→0）
2. 既存の unittest 全件パス（T1 のバグが残っている場合、その失敗は除外して判定）
