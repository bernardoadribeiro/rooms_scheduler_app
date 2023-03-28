from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()


def init_app(app):
    migrate = Migrate(app, db, directory='./rooms_scheduler_app/migrations')
    db.init_app(app)

from ..models.user import User, UserRoomPermission
from ..models.room import Room, RoomType
from ..models.schedule import Schedule
