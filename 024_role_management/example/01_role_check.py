"""
ロールベースの認可の基本（DB不使用の最小サンプル）

「本人かどうか」（所有権）と「管理者かどうか」（ロール）は別の質問です。
実際の認可判定では、この2つを組み合わせることがよくあります。

実行方法: python example/01_role_check.py
"""


class User:
    def __init__(self, id: int, username: str, is_admin: bool = False) -> None:
        self.id = id
        self.username = username
        self.is_admin = is_admin


class Post:
    def __init__(self, id: int, author_id: int) -> None:
        self.id = id
        self.author_id = author_id


def can_edit(user: User, post: Post) -> bool:
    """本人 または 管理者なら編集できる"""
    is_owner = user.id == post.author_id
    return is_owner or user.is_admin


if __name__ == '__main__':
    alice = User(id=1, username='alice')                  # 一般ユーザー
    admin = User(id=2, username='admin', is_admin=True)    # 管理者
    bob   = User(id=3, username='bob')                     # 別の一般ユーザー

    post = Post(id=100, author_id=alice.id)   # alice が書いた投稿

    print(f'alice（本人）が編集できるか: {can_edit(alice, post)}')   # True（所有権）
    print(f'admin（管理者）が編集できるか: {can_edit(admin, post)}')  # True（ロール）
    print(f'bob（他人）が編集できるか: {can_edit(bob, post)}')       # False

    assert can_edit(alice, post) is True
    assert can_edit(admin, post) is True
    assert can_edit(bob, post) is False
    print('\n所有権とロール、どちらか一方でも条件を満たせば編集できることを確認しました。')
