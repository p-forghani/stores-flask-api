from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models.store import StoreModel
from models.tag import TagModel
from models.item import ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    """Handles the tags in a store"""

    # Ensure the response follow the TagSchema
    @blp.response(200, schema=TagSchema(many=True))
    def get(self, store_id):

        # Fetch the store by its primary key (its id)
        # `db.get_or_404()` is the newer way of fetching by you can also use
        # `StoreModel.query.get_or_404(store_id)` is considered legacy
        store = db.get_or_404(StoreModel, store_id)

        tags = store.tags.all()

        # The default status code is 200, so you don't need to return it
        return tags

    # Parse, validate and inject the json payload into the function
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):

        # Return 404 if such tag with given `store_id` already exist
        if db.session.query(TagModel).filter(
            tag_data['name'] == TagModel.name,
            store_id == TagModel.store_id
        ).first():
            abort(404, message="Such tag already exists in this store")

        # Create the tag instance
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag, 201


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, schema=TagSchema)
    def get(self, tag_id):
        tag = db.get_or_404(TagModel, tag_id)
        return tag

    @blp.response(202,
                  description="Deletes a tag if no item is tagged with it",
                  example={"message": "Tag deleted"})
    @blp.alt_response(404,
                      description="Tag not found")
    @blp.alt_response(400,
                      description="Tag is assigned to one or more items")
    def delete(self, tag_id):
        tag = db.get_or_404(TagModel, tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {'message': 'Tag deleted'}
        abort(400,
              message='Could not delete tag. Make sure tag is not associated \
                with any items, then try agian.')


@blp.route("/tag")
class TagsList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        tags = db.session.query(TagModel).all()
        return tags


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

        # Ensure tag and item are in the same store
        if item.store.id != tag.store.id:
            abort(400,
                  message="Make sure item and tag belong to same store")

        # Treat the tags as a list, since its when using secondary tables
        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,
                  message="An error occured while inserting data into db")

        return tag, 201

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = db.get_or_404(ItemModel, item_id)
        tag = db.get_or_404(TagModel, tag_id)

        # Remove the tag from tags
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit(item)
        except SQLAlchemyError:
            abort(500,
                  message="An error occured while deleting the data from db")

        return {'message': "Item removed from tag",
                'item': item, 'tag': tag}
