#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)



# scientists route
@app.route('/scientists', methods=['GET'])
def get_scientists():
    scientists = Scientist.query.all()
    response = [
        {
            "id": s.id,
            "name": s.name,
            "field_of_study": s.field_of_study
        } for s in scientists
    ]
    return jsonify(response), 200
    
@app.get('/scientists')
def scientists():
    # return jsonify([s.to_dict_basic() for s in Scientist.query.all()]), 200
    return [
    {
        "id": s.id,
        "name": s.name,
        "field_of_study": s.field_of_study
    } for s in Scientist.query.all()
], 200

@app.get('/scientists/<int:id>')
def get_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    return jsonify(scientist.to_dict()), 200

@app.post('/scientists')
def create_scientist():
    data = request.json
    try:
        new_sci = Scientist(**data)
        db.session.add(new_sci)
        db.session.commit()
        return jsonify(new_sci.to_dict()), 201
    except Exception as e:
        # return jsonify({"errors": [str(e)]}), 400
        return jsonify({"errors": ["validation errors"]}), 400


@app.patch('/scientists/<int:id>')
def update_scientist(id):
    sci = Scientist.query.get(id)
    if not sci:
        return jsonify({"error": "Scientist not found"}), 404
    try:
        for k, v in request.json.items():
            setattr(sci, k, v)
        db.session.commit()
        return jsonify(sci.to_dict()), 202
    except Exception as e:
        # return jsonify({"errors": [str(e)]}), 400
        return jsonify({"errors": ["validation errors"]}), 400


@app.delete('/scientists/<int:id>')
def delete_scientist(id):
    sci = Scientist.query.get(id)
    if not sci:
        return jsonify({"error": "Scientist not found"}), 404
    db.session.delete(sci)
    db.session.commit()
    return jsonify({"message": "Scientist deleted"}), 204


@app.get('/planets')
def get_planets():
    return jsonify([p.to_dict() for p in Planet.query.all()]), 200

@app.post('/missions')
def create_mission():
    data = request.json
    try:
        mission = Mission(**data)
        db.session.add(mission)
        db.session.commit()
        return jsonify(mission.to_dict()), 201
    except Exception as e:
        # return jsonify({"errors": [str(e)]}), 400
        return jsonify({"errors": ["validation errors"]}), 400

    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
