def test_add_to_cart(logged_in_client, sample_book):
    """カートに追加すると、カート画面に書籍タイトルと小計が表示される"""
    logged_in_client.post(f'/cart/add/{sample_book.id}')
    res = logged_in_client.get('/cart/')
    assert sample_book.title.encode('utf-8') in res.data


def test_update_quantity(logged_in_client, sample_book):
    """カートの数量を更新すると、小計が正しく再計算される"""
    logged_in_client.post(f'/cart/add/{sample_book.id}')

    logged_in_client.post(f'/cart/update/{sample_book.id}', data={'quantity': '3'})
    res = logged_in_client.get('/cart/')
    assert str(sample_book.price * 3).encode('utf-8') in res.data


def test_checkout_creates_order(logged_in_client, sample_book):
    """チェックアウトすると注文が作成され、カートが空になる"""
    logged_in_client.post(f'/cart/add/{sample_book.id}')

    res = logged_in_client.post('/cart/checkout', follow_redirects=True)
    assert '注文が完了しました'.encode('utf-8') in res.data

    res2 = logged_in_client.get('/cart/')
    assert 'カートに書籍がありません'.encode('utf-8') in res2.data


def test_order_survives_price_change(logged_in_client, sample_book):
    """注文確定後に書籍の価格を変更しても、過去の注文の金額は変わらない"""
    from models import db

    logged_in_client.post(f'/cart/add/{sample_book.id}')
    logged_in_client.post('/cart/checkout')

    original_price = sample_book.price
    sample_book.price = 99999
    db.session.commit()

    res = logged_in_client.get('/cart/orders')
    assert str(original_price).encode('utf-8') in res.data
    assert b'99999' not in res.data
