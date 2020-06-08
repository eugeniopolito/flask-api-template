"""
Integration test for User
"""
from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        with self.app_context():
            user = UserModel(
                email="john.doe@email.com",
                name="John",
                surname="Doe",
                password="password",
            )

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_email("john.doe@email.com"))

    def test_delete_user(self):
        with self.app_context():
            user = UserModel(
                email="john.doe@email.com",
                name="John",
                surname="Doe",
                password="password",
            )

            user.save_to_db()
            self.assertIsNotNone(user)
            user.delete_from_db()
            user = UserModel.find_by_email("john.doe@email.com")
            self.assertIsNone(user)

    def test_update_user(self):
        with self.app_context():
            user = UserModel(
                email="john.doe@email.com",
                name="John",
                surname="Doe",
                password="password",
            )

            user.save_to_db()
            self.assertIsNotNone(user)
            new_email = "jdoe@email.com"
            user.email = new_email
            user.update()
            user = UserModel.find_by_email(new_email)
            self.assertIsNotNone(user)
