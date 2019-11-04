from flask import render_template, make_response
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('bericht',
        type=str,
        required=True, 
        help="Het bericht moet informatie bevatten!"
    )
    parser.add_argument('kleur',
        type=str,
        required=True,
        help="Kleur moet opgegeven worden!"
    )
    parser.add_argument('active',
        type=str,
        required=False,
        help="Bepaal of het bericht active moet zijn!"
    )

    def get(self, active):
        item = ItemModel.find_by_active(active)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, level):
        if ItemModel.find_by_level(level):
            return {'message': "An item with name '{}' already exists.".format(level)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(level, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    def delete(self, level):
        item = ItemModel.find_by_level(level)

        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, level):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_level(level)

        if item is None:
            item = ItemModel(level, **data)
        else:
            item.bericht = data['bericht']
            item.kleur = data['kleur']
            item.active = data['active']
        
        item.save_to_db()
        
        return item.json()


class ItemGet(Resource):
    def get(self):
        item = ItemModel.find_by_active('yes')
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


class ItemSet(Resource):
    def get(self, level):
        ItemModel.set_as_active(level)
        item = ItemModel.find_by_active('yes')
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


class ItemDiv(Resource):
    def get(self):
        item = ItemModel.find_by_active('yes')
        if item:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('template.html', bericht=item.bericht, kleur=item.kleur), 200, headers)
        return {'message': 'Item not found'}, 404



class ItemList(Resource):
    def get(self):
        return {'berichten': [x.json() for x in ItemModel.query.all()]}
    