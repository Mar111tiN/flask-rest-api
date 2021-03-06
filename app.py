from flask import Flask, jsonify
import os
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import (
        UserRegister,
        User, UserLogin,
        TokenRefresh,
        UserLogout
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from utils import seed_db
from blacklist import BLACKLIST


app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
# set the db uri based on environment - local path is default
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'mahtin'
app.secret_key = 'mahtin'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # blacklist is enabled for both token types

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    seed_db()


jwt = JWTManager(app)  # creates /auth endpoint


#  add custom associations to identities
@jwt.user_claims_loader
def add_claims_to_jwt(identity):  # should come from config file or db
    return {'is_admin': (identity == 1)}


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
        }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': "Signature verification failed.",
        'error': 'invalid_token'
        }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  #identy stored in token


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'message': "Request does not contain an access token", 
        'error': 'authorization_required' 
        }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'message': "The token is not fresh",
        'error': 'fresh_token_required'
        })


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'message': "The token has been revoked",
        'error': 'token_revoked'
        }), 401


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


# if run as a module (else run.py is used to start the program)
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
