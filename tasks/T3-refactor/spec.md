# T3: リファクタリング

## 内容

`omise/cart.py` の内部実装（`Product` を個数分リストに詰める方式）を、数量管理できる構造へ整理させる。
公開 API の互換維持とテスト不変が条件。リファクタの「質」（設計の良さ）はレビューアーの主観評価に回す。

## 検証方法（accept.py）

1. `TestCart` スイートがすべてパスすること
2. Cart の公開 API（add/remove/count/quantities/subtotal）が仕様通り動作すること
