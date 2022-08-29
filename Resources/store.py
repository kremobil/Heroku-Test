from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'new_name',
        type=str,
        required=True,
        help='set your username'
    )
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return{'message': 'An error occurred while creating store'}

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store successfully deleted'}
        return {'message': 'store does not exist'}

    def put(self, name):
        store = StoreModel.find_by_name(name)
        data = Store.parser.parse_args()
        if store:
            store.name = data['new_name']
            store.save_to_db()
        else:
            store = StoreModel(data['new_name'])
        return store.json()

class Stores(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}