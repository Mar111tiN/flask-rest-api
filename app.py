from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from models.item import ItemModel
from models.store import StoreModel


app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config['SECRET_KEY'] = 'mahtin'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    db.session
    items = [
        {"name": "chair", "price": 50.99, "store_id": 1},
        {"name": "piano", "price": 10.99, "store_id": 1},
        {"name": "pony", "price": 15.99, "store_id": 2},
        {"name": "teddy", "price": 50.99, "store_id": 2}
    ]
    stores = [
        {"name": "MusixMaker"},
        {"name": "Toys4Us"}
    ]
    for item in items:
        it = ItemModel(**item)
        it.save_to_db()
    for store in stores:
        new_store = StoreModel(**store)
        new_store.save_to_db()


jwt = JWT(app, authenticate, identity)  # creates /auth endpoint


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)    
    app.run(port=5000, debug=True)
