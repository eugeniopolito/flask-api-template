"""
User Resourse definition for Flask-RESTful
"""

import bcrypt
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from flask_restful import Resource

from lookup_tables.messages import MessageCode
from models.blacklist import BlacklistToken
from models.user import UserModel
from schemas.user import UserSchema
from support.logger import log

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    @log()
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json, partial=("registration_date",))

        if UserModel.find_by_email(user.email):
            return {"message": MessageCode.USER_EXISTS}, 400

        user.save_to_db()

        return {"message": MessageCode.USER_SUCCESSFULLY_REGISTERED}, 201


class UserLogin(Resource):

    @classmethod
    @log()
    def post(cls):
        user_json = request.get_json()
        user_data = user_schema.load(user_json, partial=("name", "surname"))

        user = UserModel.find_by_email(user_data.email)

        if user and bcrypt.checkpw(user_data.password.encode('utf8'), user.password.encode('utf8')):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": MessageCode.INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @jwt_required
    @log()
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist_token = BlacklistToken(token=jti)
        blacklist_token.save_to_db()
        return {"message": MessageCode.USER_LOGGED_OUT}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    @log()
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
