#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, request
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json()
        name = data.get("name")
        if name is None:
            return jsonify({"error": "Missing name"}), 400
        new_city = City(name=name, state_id=state_id)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    except:
        return jsonify({"error": "Not a JSON"}), 400

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    try:
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    except:
        return jsonify({"error": "Not a JSON"}), 400
