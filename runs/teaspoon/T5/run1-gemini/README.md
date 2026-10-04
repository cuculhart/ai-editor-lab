# omise

`omise` は、Pythonの学習やベンチマーク用に作成された小さなショッピングカートライブラリです。商品の管理、カートへの追加、割引計算、小計や消費税込みの合計金額の計算などをシンプルに行うことができます。

## 概要

このライブラリでは主に以下の機能を提供しています：
- **Product**: 商品名と価格を持つ商品の定義
- **Cart**: 商品をカートに追加・削除し、数量や小計を計算するショッピングカート
- **Discount**: まとめ買い時の割引率の計算や割引適用
- **Checkout**: 消費税を含めた合計金額の計算

## インストール

現在、このリポジトリはローカル環境での利用を想定しています。リポジトリをクローンまたはダウンロードし、Python環境（Python 3.10以上推奨）でご利用ください。

```bash
git clone <リポジトリのURL>
cd omise
```

## 使い方

以下に、Pythonコードを使った基本的な使い方の例を示します。

```python
from omise.cart import Cart
from omise.checkout import total_with_tax
from omise.discount import apply_bulk_discount
from omise.models import Product

# 1. 商品を作成する
apple = Product("りんご", 100)
orange = Product("みかん", 80)

# 2. ショッピングカートを作成し、商品を追加する
cart = Cart()
cart.add(apple, 3)  # りんごを3個追加
cart.add(orange, 1) # みかんを1個追加

# カート内の商品の種類数や合計個数を確認する
print(f"カート内の総商品数: {cart.count()}")  # 出力: 4

# 3. 小計を計算する
subtotal = cart.subtotal()
print(f"小計: {subtotal}円")  # 出力: 380円

# 4. まとめ買い割引を適用する（例：りんご3個に対して割引を計算する場合など）
discounted_price = apply_bulk_discount(apple.price * 3, 3)
print(f"りんご3個の割引後価格: {discounted_price}円")

# 5. 消費税込みの合計金額を計算する
total = total_with_tax(subtotal)
print(f"税込合計金額: {total}円")  # 出力: 418円
```

## テスト実行方法

このライブラリには `unittest` を使用したテストが含まれています。以下のコマンドを実行してテストが正常にパスすることを確認できます。

```bash
python -m unittest discover -s tests -t .
```

## ライセンス

このプロジェクトのライセンスについては、プロジェクト内のファイルをご確認ください。
