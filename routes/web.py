from flask import Blueprint
from controllers.menu_controller import get_all_menus
from controllers.category_controller import get_all_categories

web = Blueprint("web", __name__)

# ===========================
# MENU
# ===========================
# Get semua menu (pagination + filter)
web.route("/menus", methods=["GET"])(get_all_menus)
web.route("/categories", methods=["GET"])(get_all_categories)