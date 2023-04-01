from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pytz


db = SQLAlchemy()

# Default timezone
tz = pytz.timezone('America/Sao_Paulo')


def init_app(app):
    Migrate(app, db, directory='./rooms_scheduler_app/migrations')
    db.init_app(app)


# Import models
from ..models.user import User, UserRoomPermission
from ..models.room import Room, RoomType
from ..models.schedule import Schedule
