#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.state import State
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_cityplace(state_id=None):
    """take places from each city"""
    if storage.get(City, city_id) is None:
        abort(404)
    cityplace = []
    for p in storage.get(City, city_id).places:
        cityplace.append(p.to_dict())
    return jsonify(cityplace)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """get place object"""
    if storage.get(Placed, place_id) is None:
        abort(404)
    else:
        return jsonify(storage.get(Place, place_id).to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id=None):
    """delete place object"""
    if storage.get(Place, place_id):
        storage.delete(storage.get(Place, place_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """add city object"""
    if storage.get(City, city_id) is None:
        abort(404)
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        new_place = Place(**request.get_json())
        storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_place(city_id=None):
    """change place object"""
    if storage.get("Place", place_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key in ["id", "city_id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("Place", place_id), key, value)
    storage.save()
    return jsonify(storage.get("Place", place_id).to_dict()), 200
