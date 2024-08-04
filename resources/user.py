from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from db import db
from models.user import UserModel

from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route('/register')
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):

        # Ensure same username doesn't exist
        if UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first():
            abort(409,
                  message="A user with that username already exists.")

        user = UserModel(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password']),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occured during inserting the user in db")

        return {"message": "User created successfully"}, 201


@blp.route('/user/<int:user_id>')
class User(MethodView):
    '''
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    '''

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occured during deleting the user")
        return {'message': 'User deleted successfully'}, 200


# This is a temporary endpoint for test-only
@blp.route('/user')
class UserList(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel().query.all()


@blp.route("/login")
class login(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):

        # Retrieve the user by username
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()
        # If user exists, verify the password
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            # Return the access token to client
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        abort(401,
              message="Invalid credentials")
