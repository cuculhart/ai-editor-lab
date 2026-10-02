# Omise

ベンチマーク用の小さなショッピングカートライブラリ。

シンプルなショッピングカートをモデル化するために作成された小型 Python ライブラリです。製品の管理、/cart.py の加算、小計、および合計金額（税込み）を計算する基本機能を備えています。

## 概要

Omise は、以下の機能を持つショッピングカートを実装するための小さなライブラリです：

- 製品の追加と削除
- 製品数のカウント
- 小計金額の計算
- 税込み合計金額の計算
- 製品の数量の管理

このライブラリは、Python 3 以上で動作します。

## インストール

```bash
pip install -e .
```

または、依存関係を手動でインストールします：

- `dataclasses` (Python 3.7+ の標準ライブラリ)
- `collections` (Python 3.7+ の標準ライブラリ)

## 使い方

以下の Python コードは、ショッピングカートを基本的な方式使用する方法を示しています：

### 例 1: カートの基本的な操作

```python
from omise import Cart, Product

# カートの作成
cart = Cart()

# 製品を作成
apple = Product(name="Apple", price=100)
orange = Product(name="Orange", price=200)

# 製品をカートに追加
cart.add(apple, quantity=2)  # アップル 2 つを追加
cart.add(orange, quantity=1)  # オレンジ 1 つを追加

# カート内のアイテム数を取得
print("アイテム数:", cart.count())  # 3

# 特定の製品数のカウントを取得
print("アップルの数量:", cart.count(apple))  # 2

# カート内の製品の数量を示す辞書を取得
print("数量:", cart.quantities())  # {'Apple': 2, 'Orange': 1}

# 小計金額を計算
print("小計:", cart.subtotal())  # 400
```

### 例 2: 合計金額（税込み）の計算

```python
from omise import total_with_tax

# 合計金額（税込み）を計算
amount = 400
total = total_with_tax(amount)
print("合計金額（税込み）:", total)  # 440
```

## テスト実行方法

テストを実行するには、以下のコマンドを実行します：

```bash
python -m unittest discover -s tests -t .
```

テストは `tests` フォルダ内にあるユニットテストを実行します。

## ライセンス

MIT ライセンス
