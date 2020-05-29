"""
BlackList Token Model
"""
from support.db import db
from support.logger import log


class BlacklistToken(db.Model):
    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False, unique=True)

    @classmethod
    def find_by_id(cls, _id: int) -> "BlacklistToken":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_token(cls, token: str) -> "BlacklistToken":
        return cls.query.filter_by(token=token).first()

    @log()
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @log()
    def update(self) -> None:
        db.session.add(self)
        db.session.commit()

    @log()
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<{self.__class__.__name__}(" \
               f"token: {self.token}" \
               f")>"
