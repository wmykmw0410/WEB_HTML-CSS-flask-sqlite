from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _utcnow():
    # datetime.utcnow() はPython 3.12以降非推奨のため、
    # タイムゾーン情報付きのUTC時刻を明示的に生成する
    return datetime.now(timezone.utc)


class TrashCan(db.Model):
    __tablename__ = 'trash_cans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(10), nullable=True)
    prefecture = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    address_line = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    # ゴミの種類は複数選択できるため、キー（例: "burnable,can"）をカンマ区切りで保存する
    type = db.Column(db.String(100), nullable=False)
    photo_filename = db.Column(db.String(255), nullable=True)
    # onupdateにより、いずれかのカラムが変更されコミットされるたびに
    # SQLAlchemyが自動的に現在時刻を設定する（呼び出し側で手動更新する必要はない）
    updated_at = db.Column(db.DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)

    @property
    def full_address(self):
        return f"{self.prefecture}{self.city}{self.address_line}"
