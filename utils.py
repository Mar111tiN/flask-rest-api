import sqlite3
from contextlib import contextmanager
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel


#  @contextmanager converts functions into context managers
@contextmanager
def db_connect(db):
    # initialize a connection
    connection = sqlite3.connect(db)
    # makes the queries and store results
    cursor = connection.cursor()
    yield cursor
    connection.commit()
    connection.close()


def seed_db():
    items = [
        {'name': "chair", 'price': 50.99, 'store_id': 1},
        {'name': "piano", 'price': 10.99, 'store_id': 1},
        {'name': "pony", 'price': 15.99, 'store_id': 2},
        {'name': "teddy", 'price': 50.99, 'store_id': 2}
    ]

    stores = [
        {"name": "MusixMaker"},
        {"name": "Toys4Us"}
    ]

    users = [
        {'username': "oma", 'password': "opa"},
        {'username': "opa", 'password': "oma"}
    ]
    if ItemModel.find_all():
        return
    for store in stores:
        new_store = StoreModel(**store)
        new_store.save_to_db()

    for item in items:
        it = ItemModel(**item)
        it.save_to_db()

    for u in users:
        user = UserModel(**u)
        user.save_to_db()
