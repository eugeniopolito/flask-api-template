from models.user import UserModel
from support.ma import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "registration_date")
        load_instance = True
