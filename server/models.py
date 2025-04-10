from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', backref='planet', cascade='all, delete')
    scientists = association_proxy('missions', 'scientist')
    # Add serialization rules
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "distance_from_earth": self.distance_from_earth,
            "nearest_star": self.nearest_star
        }

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    missions = db.relationship('Mission', backref='scientist', cascade='all, delete')
    planets = association_proxy('missions', 'planet')
    # Add serialization rules
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "field_of_study": self.field_of_study,
            "missions": [mission.to_dict() for mission in self.missions]
        }
    # Add validation
    @validates('name', 'field_of_study')
    def validate_not_empty(self, key, value):
        if not value or value.strip() == "":
            raise ValueError(f"{key} cannot be empty")
        return value

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    
    # Add relationships
    # scientist = db.relationship('Scientist', back_populates='missions')
    # planet_id = db.relationship('Planet', back_populates='missions')

    # Add serialization rules
    serialize_rules = ('-scientist.missions', '-planet.missions')

    # Add validation
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == '':
            raise ValueError("Mission name cannot be empty.")
        return value

    @validates('scientist_id', 'planet_id')
    def validate_ids(self, key, value):
        if value is None:
            raise ValueError(f"{key} must not be null.")
        return value


# add any models you may need.
def to_dict_basic(self):
    return {
        "id": self.id,
        "name": self.name,
        "field_of_study": self.field_of_study
    }

Scientist.to_dict_basic = to_dict_basic