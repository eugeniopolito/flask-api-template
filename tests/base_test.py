""""
Base class test: all tests must inherit from this class.
"""
from unittest import TestCase

from app import app
from lookup_tables.api_versions import APIVersion
from support.db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["PROPAGATE_EXCEPTIONS"] = True
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context
        self.api_version = APIVersion.V1

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
