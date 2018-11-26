from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp as ssc
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True)
_user_parser.add_argument('password', type=str, required=True)


class UserRegister(Resource):
    '''saves Users from POST request to /register'''
    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': f"User {data['username']} already exits."}
        user = UserModel(**data)
        user.save_to_db()
        return {'message': f"User {user.username} created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': f"User with id {user_id} not found."}, 404
        return user.json()

    @jwt_required
    def delete(self, user_id: int):
        # stored for the delete message
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': "Admin privilege required."}, 401
        user = UserModel.find_by_id(user_id)
        if user:
            message = f"User {user.username} deleted."
            user.delete_from_db()
            return {'message': message}, 200
        return {'message': 'User not found'}, 404


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        # function of authenticate function
        if user and ssc(user.password, data['password']):
            # identity is stored in token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        # logout is accomplished by blacklisting the unique token_id (jti)
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)  # added to BLACKLIST --> should be done in db
        return {'message': 'Successfully logged out'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
