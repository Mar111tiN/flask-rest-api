import sqlite3
from flask_restful import Resource, reqparse
from utils import db_connect
from models.user import UserModel


class UserRegister(Resource):
    '''saves Users from POST request to /register'''
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': f"User {data['username']} already exits."}
        user = UserModel(**data)
        user.save_to_db()
        return {'message': f"User {user.username} created successfully."}, 201
