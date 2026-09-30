# omise

`omise` は、学習やベンチマーク用に作成された、シンプルで軽量なPython用のショッピングカートライブラリです。商品管理、カートへの商品追加・削除、数量に応じたまとめ買い割引、および消費税計算（税込金額の算出）などの基本的なECサイト機能を備えています。

---

## 概要

このプロジェクトは、Pythonの基本的な機能やテスト駆動開発（TDD）の学習、コードリーディングの練習用として設計されています。外部のサードパーティ製パッケージに依存せず、Python標準ライブラリのみで動作します。

主なコンポーネント：
- **Product** (`omise.models`): 商品情報を保持するデータクラス（商品名、税抜き価格）。
- **Cart** (`omise.cart`): カート機能。商品の追加、削除、個数カウント、小計計算などを提供。
- **Discount** (`omise.discount`): 割引ルール。一定数量以上のまとめ買いに対する割引率の計算など。
- **Checkout** (`omise.checkout`): 会計機能。小計や割引後の金額に対する税込価格の計算。

---

## インストール

外部のパッケージ依存関係はありません。リポジトリをクローンまたはダウンロードし、Pythonがインストールされている環境でお使いいただけます。

```bash
# リポジトリのクローン（例）
git clone <リポジトリのURL>
cd omise
```

---

## 使い方

以下は、`omise` ライブラリを使用してショッピングカートに商品を追加し、小計や割引、税込金額を計算する基本的なPythonコードの例です。

```python
from omise.cart import Cart
from omise.checkout import total_with_tax
from omise.discount import apply_bulk_discount
from omise.models import Product

# 1. 商品を作成する（名前、税抜き価格）
apple = Product("りんご", 150)
banana = Product("バナナ", 100)

# 2. ショッピングカートを作成する
cart = Cart()

# 3. カートに商品を追加する（商品と数量を指定）
cart.add(apple, 2)  # りんご 2個
cart.add(banana, 4)  # バナナ 4個

# カートに入っている商品の総数を確認する
print(f"総商品数: {cart.count()}個")  # 出力: 総商品数: 6個

# カートの小計（税抜き）を計算する
subtotal = cart.subtotal()
print(f"小計 (税抜): {subtotal}円")

# 4. ままとめ買い割引を適用する例（バナナ4個に対する割引）
discounted_banana_price = apply_bulk_discount(banana.price, 4)
print(f"バナナ4個（割引適用後）: {discounted_banana_price}円")

# 5. 税込金額を計算する
total_tax_included = total_with_tax(subtotal)
print(f"合計金額 (税込): {total_tax_included}円")
```

---

## テスト実行方法

このプロジェクトでは、Pythonの標準ライブラリに含まれる `unittest` を使用してテストを行っています。
プロジェクトのルートディレクトリで以下のコマンドを実行してください。

```bash
python -m unittest discover -s tests -t .
```

すべてのテストが正常にパスすることを確認できます。

---

## ライセンス

このプロジェクトは学習・ベンチマーク用であり、特記事項がない場合はオープンソース（パブリックドメインまたはMITライセンス等）として提供されています。ご利用の際はご自身の責任においてお使いください。
