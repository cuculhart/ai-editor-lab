# omise

`omise` は、Pythonでショッピングカートの機能や割引、税金計算などをシンプルなコードで試せる、初学者向けのベンチマーク用ライブラリです。

## 概要

このライブラリでは以下の機能を提供しています：
- 商品の管理（[`omise.models.Product`](omise/models.py:6)）
- ショッピングカートへの商品追加・削除・小計計算（[`omise.cart.Cart`](omise/cart.py:7)）
- まとめ買いなどの割引ルール適用（[`omise.discount`](omise/discount.py:1)）
- 消費税込みの合計金額計算（[`omise.checkout`](omise/checkout.py:1)）

## インストール

現在、このライブラリはローカルのソースコードとして提供されています。プロジェクトのディレクトリ内でそのまま利用できます。

## 使い方

以下は、商品をカートに入れて小計や税込金額、割引を計算する基本的なPythonコード例です：

```python
from omise.models import Product
from omise.cart import Cart
from omise.checkout import total_with_tax
from omise.discount import apply_bulk_discount

# 1. 商品を作成する（名前と税抜価格）
apple = Product(name="りんご", price=100)
banana = Product(name="バナナ", price=80)

# 2. ショッピングカートを作成し、商品を追加する
cart = Cart()
cart.add(apple, quantity=4)  # りんごを4個追加
cart.add(banana, quantity=2) # バナナを2個追加

# 3. カートの小計（税抜）を計算する
subtotal = cart.subtotal()
print(f"税抜小計: {subtotal}円")

# 4. 割引を適用した金額を計算する（例: りんごのまとめ買い割引）
apple_total = apply_bulk_discount(apple.price, 4)
print(f"りんご（4個・割引適用）: {apple_total}円")

# 5. 税込金額を計算する
grand_total = total_with_tax(subtotal)
print(f"税込合計: {grand_total}円")
```

## テスト実行方法

ライブラリのテストを実行するには、ターミナルで以下のコマンドを実行してください：

```bash
python -m unittest discover -s tests -t .
```

## ライセンス

MIT ライセンスです。詳細はプロジェクト内のファイルをご確認ください。

