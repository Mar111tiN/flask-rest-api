import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from utils import db_connect
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="Price is required!")
    parser.add_argument('store_id', type=int, required=True,
                        help="Store Id is required!")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': f"No {name} found in Database"}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred during insertion"}, 500  # internal server error
        return item.json(), 201

    @jwt_required()  # passes the user as current_identity into the function
    def put(self, name):
        # reqparse is used to validate the payload and only use 'price'
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        # return everything but the item to the items list
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': f'{name} deleted'}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
