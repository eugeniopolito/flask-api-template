""""
Base class test: all tests must inherit from this class.
"""
from unittest import TestCase

from app import app
from support.db import db


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
