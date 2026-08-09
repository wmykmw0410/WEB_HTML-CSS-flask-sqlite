from typing import Optional


def get_profile(
    email: str,
    username: Optional[str] = None,
    age: Optional[int] = None
    ) -> dict:
    """
    ユーザーのプロフィール情報を辞書で生成する

    Args:
        email: 必須のメールアドレス
        username: ユーザー名（指定された場合のみ含まれる）
        age: 年齢（指定された場合のみ含まれる）

    Returns:
        ユーザー情報を含む辞書。
        必ず "email" を含み、"username" と "age" は指定時のみ含まれる。
    """
    profile = {"email": email}

    if username is not None:
        profile["username"] = username

    if age is not None:
        profile["age"] = age

    return profile


#-----Calling-----
# "username" と "age" を指定しなかった場合
user_profile = get_profile(email="user@example.com")
print(user_profile)

# "username" と "age" を指定した場合
user_profile = get_profile(email="user@example.com", username="Tom", age=20)
print(user_profile)