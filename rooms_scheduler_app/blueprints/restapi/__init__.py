from flask import Blueprint
from flask_restful import Api

from .resources import UsersResource, UserResource, RoomsResource, RoomResource


bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)

# Register api routes
api.add_resource(UsersResource, "/users/")
api.add_resource(UserResource, "/users/<int:user_id>")

api.add_resource(RoomsResource, "/rooms/")
api.add_resource(RoomResource, "/rooms/<int:room_id>")

def init_app(app):
    app.register_blueprint(bp)
