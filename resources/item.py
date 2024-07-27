from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, schema=ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(schema=ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_data, item_id):
        # Fetch the item from db
        item = ItemModel.query.get(item_id)
        # Update item if exists
        if item:
            item.name = item_data['name']
            item.price = item_data['price']
        # Insert item if not exist
        else:
            item = ItemModel(id=item_id, **item_data)
        # Update info in db
        db.session.add(item)
        db.session.commit()
        # retrun item and http code
        return item


@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, schema=ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(schema=ItemSchema)
    @blp.response(201, schema=ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="Error occured while inserting the item")

        return item, 201
