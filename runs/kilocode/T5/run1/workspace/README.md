# omise

`omise` は、Pythonで書かれたシンプルで軽量なショッピングカートライブラリ（ベンチマーク用）です。商品管理、ショッピングカートへの商品追加、まとめ買い割引の計算、税込金額の計算などの基本的な機能を初学者でも分かりやすく学べる構造で提供しています。

---

## 概要

このライブラリには以下の機能が含まれています：
- **商品管理 (`Product`)**: 商品名と税抜き価格を管理します。
- **ショッピングカート (`Cart`)**: 商品の追加・削除、数量確認、小計計算を行います。
- **割引ルール (`discount`)**: 一定条件でのまとめ買い割引計算を行います。
- **会計計算 (`checkout`)**: 税込金額の計算を行います。

---

## インストール

本リポジトリをローカル環境にクローンしてご利用いただけます。外部の追加パッケージは不要で、Python 3.8以上の標準ライブラリのみで動作します。

```bash
git clone <repository-url>
cd T5
```

---

## 使い方（Python のコード例付き）

以下に、商品の登録、ショッピングカートへの商品追加、小計および税込金額の計算を行う基本的な使い方を示します。

```python
from omise.cart import Cart
from omise.checkout import total_with_tax
from omise.models import Product

# 1. 商品を作成する（引数: 商品名, 税抜き価格）
apple = Product("りんご", 100)
orange = Product("みかん", 80)

# 2. ショッピングカートを作成する
cart = Cart()

# 3. カートに商品を追加する（例: りんごを3個、みかんを2個追加）
cart.add(apple, 3)
cart.add(orange, 2)

# 4. カート内の商品数や小計を確認する
print(f"総商品数: {cart.count()}個")        # 出力: 5個
print(f"小計（税抜き）: {cart.subtotal()}円") # 出力: 460円

# 5. 税込金額を計算する（消費税10%）
subtotal = cart.subtotal()
total = total_with_tax(subtotal)
print(f"合計（税込）: {total}円")
```

---

## テスト実行方法

このプロジェクトには、動作確認用のユニットテストが含まれています。以下のコマンドをプロジェクトのルートディレクトリで実行してテストを行うことができます。

```bash
python -m unittest discover -s tests -t .
```

---

## ライセンス

This project is licensed under the MIT License.
