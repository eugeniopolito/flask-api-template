from dotenv import load_dotenv
from flask import Flask, __version__
from flask import jsonify, render_template
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from marshmallow import ValidationError

from lookup_tables.api_versions import APIVersion
from lookup_tables.messages import MessageCode
from models.blacklist import BlacklistToken
from resources.user import UserRegister, UserLogin, TokenRefresh, UserLogout
from support.db import db

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py

api = Api(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

""""
Create all DB tables before the first request.
"""


@app.before_first_request
def create_tables():
    db.create_all()


"""
JWT Extendend tokens related handlers.
"""


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    return {"identity": identity}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": MessageCode.TOKEN_EXPIRED}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": MessageCode.TOKEN_INVALID}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": MessageCode.AUTHORIZATION_REQUIRED}), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({"message": MessageCode.TOKEN_NOT_FRESH}), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({"message": MessageCode.TOKEN_REVOKED}), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return BlacklistToken.find_by_token(decrypted_token["jti"])


"""
Specific error handlers.
"""


@app.errorhandler(ValidationError)
def marshmallow_validation_error_handler(err):
    return jsonify(err.messages), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.jinja2"), 404


@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.jinja2"), 401


"""
Public APIs
"""


@app.route("/")
def home():
    return render_template("info.jinja2", flask_version=__version__), 200


api.add_resource(UserRegister, f"{APIVersion.V1}/register")
api.add_resource(UserLogin, f"{APIVersion.V1}/login")
api.add_resource(UserLogout, f"{APIVersion.V1}/logout")
api.add_resource(TokenRefresh, f"{APIVersion.V1}/refresh")
