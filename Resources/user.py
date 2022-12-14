import sqlite3
from flask_restful import Resource, reqparse
from models.usermodel import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', type=str,
        required=True,
        help='set your username'
    )
    parser.add_argument(
        'password', type=str,
        required=True,
        help='set your password',
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": f"username {data['username']} already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "user craeted successfully"}, 201

