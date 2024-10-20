from flask import jsonify
from api import app, db, request, multi_auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema
from flask_apispec  import doc, marshal_with, use_kwargs


@app.route("/users/<int:user_id>")
@doc(description='Api for getting only user.', tags=['Users'], summary="Get user by id")
@marshal_with(UserSchema, code=200)
def get_user_by_id(user_id):
    user = db.get_or_404(UserModel, user_id, description=f"User with id={user_id} not found")
    return user, 200


@app.route("/users")
def get_users():
    """
    Get all Users
    ---
    tags:
        - Users
    """
    users = db.session.scalars(db.select(UserModel)).all()
    return users_schema.dump(users), 200


@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.json
    user = UserModel(**user_data)
    # TODO: добавить обработчик на создание пользователя с неуникальным username
    if db.session.scalars(db.select(UserModel).where(UserModel.username==user.username)).one_or_none():
        return {"error": "User already exists."}, 409
    user.save()
    return user_schema.dump(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required(role="admin")
def edit_user(user_id):
    user_data = request.json
    user = db.get_or_404(UserModel, user_id, description=f"Note with id={user_id} not found")
    for key, value in user_data.items():
        setattr(user, key, value)
    user.save()
    return user_schema.dump(user), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
def delete_user(user_id):
    """
    Пользователь может удалять ТОЛЬКО свои заметки
    Алгоритм:
    1. Получить автора заметки
    2. Удалить автора, вызвав метод delete()
    3. Вернуть сообщние об этом.
    """
    user = db.get_or_404(UserModel, user_id, description=f"Note with id={user_id} not found")
    user.delete()
    return jsonify({"message": f"User with={user_id} has deleted."}), 200