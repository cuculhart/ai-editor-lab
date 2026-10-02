# Omise（ショッピングカートライブラリ）

初学者向けに作成された、Python用のシンプルなショッピングカート・割引・会計計算ライブラリです。

## 概要

`omise` は、ECサイトや店舗システムで必要となる基本的な機能をモジュールとして提供する、学習用・ベンチマーク用の小さなプロジェクトです。

主な機能：
- **商品管理** (`omise.models`): 商品名と税抜き価格を持つデータクラス
- **ショッピングカート** (`omise.cart`): 商品の追加、削除、数量確認、小計計算
- **割引計算** (`omise.discount`): まとめ買い割引（例: 3個以上で10%OFF）の判定と適用
- **会計計算** (`omise.checkout`): 消費税（10%）を含めた税込金額の計算

---

## インストール

このプロジェクトは外部ライブラリに依存していません（Python標準ライブラリのみを使用します）。
Python 3.8以上がインストールされている環境で、ソースコードをクローンまたはダウンロードしてそのままご利用いただけます。

```bash
# リポジトリのクローン（例）
git clone <repository-url>
cd T5
```

---

## 使い方（Python のコード例付き）

以下に、商品の定義からショッピングカートへの追加、割引適用、そして税込の合計金額を計算するまでの基本的な使い方を示します。

```python
from omise.models import Product
from omise.cart import Cart
from omise.discount import apply_bulk_discount
from omise.checkout import total_with_tax

# 1. 商品を作成する（引数: 商品名, 税抜き価格）
apple = Product("りんご", 120)
banana = Product("バナナ", 80)

# 2. ショッピングカートを作成し、商品を追加する
cart = Cart()
cart.add(apple, 3)  # りんごを3個追加
cart.add(banana, 2) # バナナを2個追加

# カート内の商品の小計（税抜き）を計算する
subtotal = cart.subtotal()
print(f"小計（税抜き）: {subtotal}円")  # 出力: 520円 (120*3 + 80*2)

# 3. まとめ買い割引を適用する（りんごを3個買った場合の割引後価格）
discounted_apple_price = apply_bulk_discount(apple.price, 3)
print(f"りんご3個（割引適用後）: {discounted_apple_price}円")  # 出力: 324円 (120 * 3 * 0.9)

# 4. 税込金額を計算する
total = total_with_tax(subtotal)
print(f"合計（税込）: {total}円")  # 出力: 572円 (520 * 1.1 の小数点以下切り捨て)
```

---

## テスト実行方法

このプロジェクトでは、Python標準の `unittest` ライブラリを使用してテストを記述しています。
プロジェクトのルートディレクトリで以下のコマンドを実行し、すべてのテストが正常にパスすることを確認できます。

```bash
python -m unittest discover -s tests -t .
```

---

## ライセンス

このプロジェクトは学習・ベンチマーク用として公開されており、オープンソース（詳細なライセンス条件はプロジェクトの規定に準じます）です。

