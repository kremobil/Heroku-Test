from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from Resources.user import UserRegister
from Resources.item import Item, Items
from Resources.store import Store, Stores
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'wiktor'
api = Api(app)

@app.before_first_request
def crate_tabels():
    db.create_all()

app.config['JWT_AUTH_URL_RULE'] = '/login'

jwt = JWT(app, authenticate, identity)  # /auth

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)


@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return {'access_token': access_token.decode('utf-8'), 'user_id': identity.id}

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(Stores, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
