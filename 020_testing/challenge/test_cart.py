"""
練習問題：カート・チェックアウトのテストを書こう

以下の TODO コメントの箇所にコードを書いて、テストを完成させてください。
（`pytest.fail(...)` の行は目印です。実装できたら削除してください。
 何も書かずに `pass` のままにすると、アサーションが1つも実行されず
 テストが「成功」してしまう点に注意してください。）

実行方法: pytest test_cart.py -v
"""
import pytest


def test_add_to_cart(logged_in_client, sample_book):
    """カートに追加すると、カート画面に書籍タイトルと小計が表示される"""
    # TODO: logged_in_client.post(f'/cart/add/{sample_book.id}') でカートに追加する
    # TODO: logged_in_client.get('/cart/') でカート画面を取得する
    # TODO: レスポンスに sample_book.title が含まれることを確認する
    pytest.fail('TODO: 実装してください')


def test_update_quantity(logged_in_client, sample_book):
    """カートの数量を更新すると、小計が正しく再計算される"""
    logged_in_client.post(f'/cart/add/{sample_book.id}')  # まず1件追加しておく

    # TODO: logged_in_client.post(f'/cart/update/{sample_book.id}', data={'quantity': '3'}) で数量を3に更新する
    # TODO: logged_in_client.get('/cart/') でカート画面を取得する
    # TODO: 合計金額（sample_book.price * 3）の文字列がレスポンスに含まれることを確認する
    pytest.fail('TODO: 実装してください')


def test_checkout_creates_order(logged_in_client, sample_book):
    """チェックアウトすると注文が作成され、カートが空になる"""
    logged_in_client.post(f'/cart/add/{sample_book.id}')

    # TODO: logged_in_client.post('/cart/checkout', follow_redirects=True) で注文を確定する
    # TODO: レスポンスに '注文が完了しました' が含まれることを確認する

    # TODO: logged_in_client.get('/cart/') でカート画面を取得し、
    #       'カートに書籍がありません' が含まれることを確認する（カートが空になっている）
    pytest.fail('TODO: 実装してください')


def test_order_survives_price_change(logged_in_client, sample_book):
    """注文確定後に書籍の価格を変更しても、過去の注文の金額は変わらない"""
    from models import db

    logged_in_client.post(f'/cart/add/{sample_book.id}')
    logged_in_client.post('/cart/checkout')

    original_price = sample_book.price
    sample_book.price = 99999
    db.session.commit()

    # TODO: logged_in_client.get('/cart/orders') で注文履歴を取得する
    # TODO: レスポンスに original_price が含まれ、99999は含まれないことを確認する
    pytest.fail('TODO: 実装してください')
