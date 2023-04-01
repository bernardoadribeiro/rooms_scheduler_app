from flask import jsonify, abort, request
from flask_restful import Resource

from rooms_scheduler_app.ext.database import User
from ...ext.auth import create_user


class UsersResource(Resource):
    """ Users Resource"""

    def get(self):
        users = User.query.all() or abort(204)

        return jsonify(
            {'users': [
                user.to_dict()
                for user in users
            ]}
        )

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, "No data received in the body.")

        username = data.get('username')
        password = data.get('password')

        new_user = create_user(username, password)

        return jsonify(new_user.to_dict())


class UserResource(Resource):
    """ User resource. Returns a single user."""

    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first() or abort(404)

        return jsonify(user.to_dict())
