from app import app
from db import db

db.init_app(app)


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
