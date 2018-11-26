from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
    )
from typing import Dict
from utils import db_connect
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="Price is required!")
    parser.add_argument('store_id', type=int, required=True,
                        help="Store Id is required!")

    def get(self, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': f"No {name} found in Database"}, 404

    @fresh_jwt_required
    def post(self, name: str):
        if ItemModel.find_by_name(name):
            return {'message': f'An item {name} already exists'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred during insertion"}, 500  # internal server error
        return item.json(), 201

    @jwt_required  # passes the user as current_identity into the function
    def put(self, name: str):
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

    @jwt_required
    def delete(self, name: str):
        # return everything but the item to the items list
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'{name} deleted'}, 200
        return {'message': 'Item {} not found.'.format(name)}, 404


class ItemList(Resource):
    @jwt_optional  # jwt_token gives more funtionality but is optional
    def get(self):
        user_id = get_jwt_identity()  # getting id from jwt_token
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200  # full info for logged in users
        return {
            'items': [item['name'] for item in items],
            'message': "More info for logged-in users!"}, 200
