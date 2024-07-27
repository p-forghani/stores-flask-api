from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)

    # The `cascade="all, delete"` ensures that all items of the
    # store are deleted when the store is deleted. The cascade should be added
    # to the `relationship()` call in the parent model of a one-to-many
    # relationship.

    # `cascade="delete-orphan"` ensures ensure that an item is deleted from
    # database if it is removed from its store

    # `back_populates` specifies the relationship between the store and item.

    # `lazy="dynamic"` means that the items will be loaded dynamically and
    # only when accessed, which can help improve performance when dealing
    # with large datasets.
    items = db.relationship("ItemModel",
                            back_populates="store",
                            lazy="dynamic",
                            cascade="all, delete, delete-orphan")
    # `back_populates` should be correspond property in the other model of the
    # relationship; in this case the `store` property in the TagModel
    tags = db.relationship("TagModel",
                           back_populates="store",
                           lazy="dynamic")
