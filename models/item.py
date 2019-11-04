from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(10))
    bericht = db.Column(db.String(80))
    kleur = db.Column(db.String(20))
    active = db.Column(db.String(8))

    def __init__(self, level, bericht, kleur, active):
        self.level = level
        self.bericht = bericht
        self.kleur = kleur
        self.active = active

    def json(self):
        return {'id': self.id, 'level': self.level,'bericht': self.bericht, 'kleur': self.kleur, 'active': self.active}

    @classmethod
    def find_by_level(cls, level):
        return cls.query.filter_by(level=level).first()

    @classmethod
    def find_by_active(cls, active):
        return cls.query.filter_by(active=active).first()

    @classmethod
    def set_as_active(cls, level):
        cls.query.update(dict(active='no'))
        item = cls.query.filter_by(level=level).update(dict(active='yes'))
        db.session.commit()
        return item

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
