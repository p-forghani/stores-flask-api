from db import db


class ItemsTags(db.Model):
    __tablename__ = 'items_tags'

    id = db.Column(db.Integer, primary_key=True)
    # `items.id` refers to id column of tablename items
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
