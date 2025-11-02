from flask import request, jsonify
from sqlalchemy.orm import Session, joinedload
from config.database import get_db
from models.menu_model import Menu

def get_all_menus():
    db: Session = next(get_db())
    q = db.query(Menu).options(joinedload(Menu.category))

    # --- filters ---
    search = request.args.get("search")
    if search:
        q = q.filter(Menu.name.ilike(f"%{search}%"))

    category = request.args.get("category_id")
    if category:
        try:
            q = q.filter(Menu.category_id == int(category))
        except ValueError:
            return jsonify({"error": "category_id must be integer"}), 400

    price_from = request.args.get("price_from")
    if price_from:
        try:
            q = q.filter(Menu.price >= int(price_from))
        except ValueError:
            return jsonify({"error": "price_from must be integer"}), 400

    price_to = request.args.get("price_to")
    if price_to:
        try:
            q = q.filter(Menu.price <= int(price_to))
        except ValueError:
            return jsonify({"error": "price_to must be integer"}), 400

    # --- pagination ---
    try:
        page = int(request.args.get("page", 1))
        size = int(request.args.get("size", 10))
        if page < 1 or size < 1:
            raise ValueError
    except ValueError:
        return jsonify({"error": "page and size must be positive integers"}), 400

    total = q.count()
    items = q.offset((page - 1) * size).limit(size).all()

    data = [m.to_dict() for m in items]

    meta = {
        "current_page": page,
        "per_page": size,
        "total_pages": (total + size - 1) // size if size else 0,
        "total_items": total
    }

    return jsonify({
        "message": "Success get menus",
        "data": data,
        "meta": meta
    }), 200
