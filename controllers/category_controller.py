from flask import jsonify
from sqlalchemy.orm import Session
from config.database import get_db
from models.category_model import Category

def get_all_categories():
    db: Session = next(get_db())
    categories = db.query(Category).all()

    return jsonify({
        "message": "Success get categories",
        "data": [c.to_dict() for c in categories]
    }), 200
