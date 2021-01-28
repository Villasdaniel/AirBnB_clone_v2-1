#!/usr/bin/python3
"""users"""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """get user object"""
    if user_id is None:
        Nuserlist = []
        for item in storage.all(User).values():
            Nuserlist.append(item.to_dict())
        return jsonify(Nuserlist)
    elif storage.get(User, user_id):
        return jsonify(storage.get(User, user_id).to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id=None):
    """Delete user object"""
    if storage.get(User, user_id):
        storage.delete(storage.get(User, user_id))
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Add user object"""
    if request.get_json() is None:
        abort(400, "Not a JSON")
    elif "name" not in request.get_json().keys():
        abort(400, "Missing name")
    else:
        new_user = User(**request.get_json())
        storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id=None):
    """Update user object"""
    if storage.get("User", user_id) is None:
        abort(404)
    if request.get_json() is None:
        return "Not a JSON", 400
    for key, value in request.get_json().items():
        if key in ["id", "created_at", "updated_at"]:
            pass
        else:
            setattr(storage.get("User", user_id), key, value)
    storage.save()
    return jsonify(storage.get("User", user_id).to_dict()), 200
