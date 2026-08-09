"""
pytest の基本

実行方法:
    pytest example/test_01_pytest_basics.py -v
"""


def add(a: int, b: int) -> int:
    return a + b


# ------------------------------------------------------------
# 1. テスト関数は `test_` から始める名前で書く
#    assert が失敗すると、そのテストは FAILED になる
# ------------------------------------------------------------
def test_add():
    assert add(2, 3) == 5


def test_add_with_negative():
    assert add(-1, 1) == 0


# ------------------------------------------------------------
# 2. 例外が発生することを確認したいときは pytest.raises を使う
# ------------------------------------------------------------
import pytest


def divide(a: int, b: int) -> float:
    return a / b


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


# ------------------------------------------------------------
# 3. フィクスチャ（fixture）— テストの前処理を共通化する
#    引数名がそのままフィクスチャ名になり、戻り値が渡ってくる
# ------------------------------------------------------------
@pytest.fixture
def sample_list() -> list[int]:
    return [3, 1, 4, 1, 5, 9]


def test_sample_list_length(sample_list):
    assert len(sample_list) == 6


def test_sample_list_max(sample_list):
    assert max(sample_list) == 9


# ------------------------------------------------------------
# 4. parametrize — 同じテストを複数の入力パターンで実行する
# ------------------------------------------------------------
@pytest.mark.parametrize('a, b, expected', [
    (1, 1, 2),
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
