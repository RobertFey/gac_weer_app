from flask import Flask
from flask_restful import Api
from resources.item import Item, ItemList, ItemGet, ItemDiv, ItemSet


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, '/item/<string:level>')
api.add_resource(ItemSet, '/item/set/<string:level>')
api.add_resource(ItemDiv, '/item/html/')
api.add_resource(ItemGet, '/item/json/')
api.add_resource(ItemList, '/items/json/')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
