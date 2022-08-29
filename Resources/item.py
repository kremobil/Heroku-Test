from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price', type=float,
        required=True,
        help='set the item price'
    )
    parser.add_argument(
        'store_id', type=int,
        required=True,
        help='link our item to store by id'
    )

    @jwt_required()
    def get(self, name: str):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item does not exist'}, 404

    def post(self, name: str):
        if ItemModel.find_item_by_name(name):
            return {"message": "item already exists in database"}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while adding item"}, 500
        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'items were deleted successfully'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price, item.store_id = data.values()
        item.save_to_db()

        return item.json()


class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}, 200
