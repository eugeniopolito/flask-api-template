"""
BlackList Token Model
"""
from support.db import db
from support.logger import log


class BlacklistToken(db.Model):
    """
    The BlacklistToken class model.
    This class is used for logging out user by token blacklisting.
    """

    __tablename__ = "blacklist_tokens"

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False, unique=True)

    @classmethod
    def find_by_id(cls, _id: int) -> "BlacklistToken":
        """
        Find a token by id.
        :param _id: the token id to search for
        :return: a BlacklistToken object
        """
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_token(cls, token: str) -> "BlacklistToken":
        """
        Find a token by value.
        :param token: the token value to search for
        :return: a BlacklistToken object
        """
        return cls.query.filter_by(token=token).first()

    @log()
    def save_to_db(self) -> None:
        """
         Save a token into database.
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    @log()
    def delete_from_db(self) -> None:
        """
        Delete a token.
        :return: None
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<{self.__class__.__name__}(" f"token: {self.token}" f")>"
