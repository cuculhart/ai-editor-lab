# omise

ベンチマーク用の小さなショッピングカートライブラリです。Pythonの基礎学習やテストの練習にも適しています。

## 概要

`omise` は、オンラインショップの基本的なショッピングカート機能（商品の管理、小計計算、割引、税込計算など）を提供するシンプルなPythonパッケージです。

主なモジュールと機能:
- **商品管理 (`omise.models`)**: 商品名と税抜き価格を保持する `Product` クラスを提供します。
- **ショッピングカート (`omise.cart`)**: カートへの商品の追加、削除、数量確認、小計計算を行う `Cart` クラスを提供します。
- **割引ルール (`omise.discount`)**: まとめ買い割引などの割引率計算や適用を行います。
- **会計 (`omise.checkout`)**: 消費税を考慮した税込金額の計算を行います。

## インストール

このプロジェクトは外部ライブラリに依存せず、Python標準機能のみで動作します。
Python 3.8以上の環境で、プロジェクトのソースコードを任意のディレクトリに配置してご利用ください。

```bash
git clone <repository-url>
cd <project-directory>
```

## 使い方（Python のコード例付き）

以下は、商品を作成してカートに追加し、小計や税込金額を計算する基本的な使い方の例です。

```python
from omise.models import Product
from omise.cart import Cart
from omise.checkout import total_with_tax

# 1. 商品を作成する（名前、税抜き価格）
apple = Product("りんご", 100)
orange = Product("みかん", 80)

# 2. ショッピングカートを作成し、商品を追加する
cart = Cart()
cart.add(apple, 3)   # りんごを3個追加
cart.add(orange, 2)  # みかんを2個追加

# 3. カートの件数や小計（税抜き）を計算する
print(f"商品総数: {cart.count()} 個")          # 出力: 5 個
print(f"小計（税抜き）: {cart.subtotal()} 円")   # 出力: 460 円

# 4. 税込金額を計算する（消費税10%）
subtotal_price = cart.subtotal()
total_price = total_with_tax(subtotal_price)
print(f"合計（税込）: {total_price} 円")       # 出力: 506 円
```

## テスト実行方法

このプロジェクトのテストは Python 標準の `unittest` ライブラリを使用して書かれています。
テストを実行するには、プロジェクトのルートディレクトリで以下のコマンドを実行してください。

```bash
python -m unittest discover -s tests -t .
```

すべてのテストが正常に完了すると、次のような出力が表示されます。

```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
```

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。
