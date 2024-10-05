from api import app, db, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema


@app.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = db.get_or_404(UserModel, user_id, description=f"Note with id={user_id} not found")
    return user_schema.dump(user), 200


@app.route("/users")
def get_users():
    users = db.session.scalars(db.select(UserModel)).all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    user = UserModel(**user_data)
    # TODO: добавить обработчик на создание пользователя с неуникальным username
    user.save()
    return user_schema.dump(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required(role="admin")
def edit_user(user_id):
    user_data = request.json
    user = db.get_or_404(UserModel, user_id, description=f"Note with id={user_id} not found")
    user.username = user_data["username"]
    user.save()
    return user_schema.dump(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    """
    Пользователь может удалять ТОЛЬКО свои заметки
    """
    raise NotImplemented("Метод не реализован")