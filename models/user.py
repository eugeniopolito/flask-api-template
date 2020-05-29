"""
User Model
"""
import time

import bcrypt

from support.db import db
from support.logger import log


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.BigInteger, nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "User":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        return cls.query.filter_by(email=email).first()

    @log()
    def save_to_db(self) -> None:
        db.session.add(self)
        self.password = bcrypt.hashpw(self.password.encode('utf8'), bcrypt.gensalt())
        self.password = self.password.decode("utf-8", "ignore")
        self.registration_date = int(round(time.time()))
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
               f"name: {self.name}, " \
               f"surname: {self.surname}, " \
               f"email: {self.email}" \
               f")>"
