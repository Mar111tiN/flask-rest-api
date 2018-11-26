from app import app
from db import db
from utils import seed_db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
    seed_db()
