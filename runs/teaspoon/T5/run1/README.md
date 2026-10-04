# omise

ベンチマーク用のシンプルなショッピングカートライブラリです。Python で書かれています。

## 概要

このライブラリは、ベンチマークテスト用に設計されたショッピングカートシステムを提供します。以下の基本的な機能をサポートします:

- チェックアウト（商品カートの追加・管理）
- 割引計算
- 決済チェック

## インストール

このライブラリをインストールするには、以下のコマンドを実行します:

```bash
pip install -e .
```

または、Python バージョン 3.7 以降が必要です。

## 使い方

以下は、基本的な使い方です。

```python
from omise import Checkout, Discount

# シャルドの作成
checkout = Checkout(
    merchant_id="MERCHANT_ID",
    email="user@example.com"
)

# ショッピングカートを追加
cart = checkout.add_items(
    id="ITEM_1",
    name="商品 A",
    price=1000
)

# 割引
discount = Discount(amount=20)

# 決済チェック
result = checkout.checkout(cart, discount)
```

## テスト実行方法

```bash
python -m unittest discover -s tests -t .
```

## ライセンス

MIT License
