from app import app
from support.db import db
from support.ma import ma

db.init_app(app)
ma.init_app(app)
