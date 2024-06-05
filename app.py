from flask import Flask, request
from db import stores, items
from flask_smorest import abort
import uuid


app = Flask(__name__)


@app.get("/store")
def get_stores():
    '''Return all the stores'''
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    '''Create a new store'''
    request_data = request.get_json()  # sample_valid_json = {'name': 'luna'}
    store_id = uuid.uuid4().hex
    new_store = {**request_data, 'store_id': store_id}

    # Handle KeyError
    if (
        'name' not in new_store
        or 'store_id' not in new_store
    ):
        abort(400,
              message="Bad request, ensure <name> and <store_id> keys included in json")
    # Handle duplicate stores
    for store in stores:
        if (new_store['name'] == store['name'] and
                new_store['store_id'] == store['store_id']):
            abort(400, "Store with such name and store_id exists")

    stores[store_id] = new_store
    return {"store": new_store}, 201


@app.post("/item")
def create_item():
    '''Create an item'''
    request_data = request.get_json()  # ie: {"name": "laptop", "price": 3}
    item_id = uuid.uuid4().hex
    new_item = {**request_data, 'item_id': item_id}
    if (
        'name' not in new_item
        or 'price' not in new_item
        or 'item_id' not in new_item
    ):
        abort(400,
              message="Bad request; Ensure price and name keys are included")

    for item in items:
        if (
            new_item['name'] == item['name']
            and new_item['item_id'] == item['item_id']
        ):
            abort(400,
                  message="Bad request; This item already exist")
    items[item_id] = new_item
    return {"item": new_item}, 201


@app.get("/store/<string:store_id>")
def get_store(store_id):
    """Retrieve a store by its id"""
    try:
        return stores[store_id], 200
    except KeyError:
        return {"message": "Store not found"}, 404

@app.get("/item")
def get_all_items():
    return list(items.values())


@app.get('/item/<string:item_id>')
def get_item(item_id):
    '''Retrieve item by its id'''
    try:
        return items[item_id], 200
    except KeyError:
        return {"message": "Store not found"}, 404
