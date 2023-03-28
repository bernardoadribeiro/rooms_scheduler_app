from flask import Blueprint
from flask_restful import Api

from .resources import UsersResource, UserResource


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)

# register api routes
api.add_resource(UsersResource, "/users/")
api.add_resource(UserResource, "/users/<user_id>")

def init_app(app):
    app.register_blueprint(bp)
