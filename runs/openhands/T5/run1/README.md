# omise

`omise` は、Pythonで書かれたシンプルで軽量なショッピングカートライブラリです。ベンチマークや学習用途を想定して設計されています。

---

## 概要

`omise` ライブラリを使うことで、以下のショッピングカート関連の処理を簡単に実装できます：
- 商品の管理（商品データの定義、カートへの商品追加・削除）
- カート内の集計（数量の確認、小計の算出）
- 割引計算（まとめ買い割引などのルール適用）
- 会計処理（消費税込みの合計金額計算）

---

## インストール

本ライブラリはローカルのソースコードとして提供されています。ご利用の環境にクローンまたは配置し、Pythonからインポートして使用してください。

プロジェクトのルートディレクトリで作業している場合、Pythonのモジュールとして直接読み込むことができます。

---

## 使い方（Python のコード例付き）

以下に、商品の追加から小計計算、割引、税込金額の計算までの基本的な使い方を示します。

```python
from omise.models import Product
from omise.cart import Cart
from omise.discount import apply_bulk_discount, bulk_discount_rate
from omise.checkout import total_with_tax

# 1. 商品を作成する（引数: 商品名, 税抜価格）
apple = Product("りんご", 100)
orange = Product("みかん", 80)

# 2. ショッピングカートを作成し、商品を追加する
cart = Cart()
cart.add(apple, quantity=3)   # りんごを3個追加
cart.add(orange, quantity=1)  # みかんを1個追加

# 3. カートの情報を確認する
print("商品別の数量:", cart.quantities())  # 例: {'りんご': 3, 'みかん': 1}
print("総アイテム数:", cart.count())       # 4
print("小計（税抜）:", cart.subtotal(), "円") # 380 円

# 4. まとめ買い割引を適用する（例: りんご3個の場合の割引率や割引後価格）
rate = bulk_discount_rate(3)
print("りんご3個の割引率:", f"{int(rate * 100)}%")

discounted_price = apply_bulk_discount(apple.price, 3)
print("りんご3個の割引後価格（税抜）:", discounted_price, "円")

# 5. 税込の合計金額を計算する（消費税率 10%）
subtotal = cart.subtotal()
total = total_with_tax(subtotal)
print("税込合計金額:", total, "円")
```

---

## テスト実行方法

このプロジェクトにはユニットテストが含まれています。テストを実行するには、プロジェクトのルートディレクトリで以下のコマンドを実行してください。

```bash
python -m unittest discover -s tests -t .
```

---

## ライセンス

本ソフトウェアは学習およびベンチマーク用ライブラリです。自由にご利用・改変いただけます。

