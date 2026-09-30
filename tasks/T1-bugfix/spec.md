# T1: バグ修正

## 内容

`omise/discount.py` の `bulk_discount_rate` に境界値バグ（`> 3` であるべきところ `>= 3` の仕様）を仕込んである。
「3個以上で10%引き」のはずが3個ちょうどで割引が効かず、`tests/test_omise.py` の境界値テストが失敗する。

## 検証方法（accept.py）

1. `tests/` 以下が fixture の原本から改変されていないこと
2. `python -m unittest discover -s tests -t .` が全件パスすること
