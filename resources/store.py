from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from schemas import StoreSchema
from models import StoreModel
from db import db

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):

    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        # Fetch the store from db
        # Return 404 if store don't exist
        store = StoreModel.query.get_or_404(store_id)
        # Return store and http code
        return store, 200

    def delete(cls, store_id):
        store = StoreModel.query.get_or_404(store_id)  # noqa
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return StoreModel().query.all()

    @blp.arguments(schema=StoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,
                  message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500,
                  message="An error occured while creating the store")
        return store, 201
