from api import ma
from api.models.user import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        fields = ('id', 'username', "role")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Десериализация запроса(request)
class UserRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    username = ma.Str()
    password = ma.Str()
    role = ma.Str()
