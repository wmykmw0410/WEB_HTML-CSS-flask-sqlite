"""
パスワードのハッシュ化 — werkzeug.security

実行:
    python example/01_password_hash.py
"""
from werkzeug.security import generate_password_hash, check_password_hash

raw: str = 'mypassword123'

# --------------------------------------------------
# 1. ハッシュ化（DB に保存する値）
# --------------------------------------------------
hashed: str = generate_password_hash(raw)
print('=== ハッシュ化 ===')
print('平文  :', raw)
print('ハッシュ:', hashed)

# --------------------------------------------------
# 2. 照合（ログイン時）
# --------------------------------------------------
print('\n=== 照合 ===')
print('正しいパスワード:', check_password_hash(hashed, raw))       # True
print('違うパスワード  :', check_password_hash(hashed, 'wrong'))   # False

# --------------------------------------------------
# 3. 同じパスワードでも毎回ハッシュが異なる（ソルト付き）
# --------------------------------------------------
hash2 = generate_password_hash(raw)
print('\n=== ソルトの確認 ===')
print('1回目:', hashed[:40], '...')
print('2回目:', hash2[:40], '...')
print('ハッシュ同士は一致するか :', hashed == hash2)          # False
print('check_password_hash なら:', check_password_hash(hash2, raw))  # True
