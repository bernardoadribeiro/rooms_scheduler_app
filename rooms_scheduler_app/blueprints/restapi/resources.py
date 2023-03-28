from flask import jsonify, abort
from flask_restful import Resource
from rooms_scheduler_app.ext.database import User

# APIs Resources

# Users
class UsersResource(Resource):
    """ Users Resource"""
    def get(self):
        users = User.query.all() or abort(204)

        return jsonify(
            {'users':[ 
                user.to_dict()
                for user in users
            ]}
        )

class UserResource(Resource):
    """ User resource. Returns a single user."""
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first() or abort(404)
        
        return jsonify(user.to_dict())
    