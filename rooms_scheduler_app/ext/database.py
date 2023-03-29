from datetime import datetime
from typing_extensions import override
import pytz

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# Default timezone
tz = pytz.timezone('America/Sao_Paulo')

def init_app(app):
    migrate = Migrate(app, db, directory='./rooms_scheduler_app/migrations')
    db.init_app(app)


# Database models

# User models
class User(db.Model, SerializerMixin):
    """ Users model class"""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    type = db.Column(db.String()) # Admin, Teacher, Student

    @override
    def to_dict(self):
        """Return user information as dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
            'type': self.type
        }


class UserRoomPermission(db.Model, SerializerMixin):
    """ Users Rooms Permissions Permissions class"""

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'),
        nullable=False)
    room_type = db.relationship('RoomType', lazy=True)


#  Room models
class Room(db.Model, SerializerMixin):
    """ Rooms model class"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'),
        nullable=False)
    room_type = db.relationship('RoomType', lazy=True)
    key_status = db.Column(db.String()) # Lost, On_Hand, Scheduled
    room_status = db.Column(db.String()) # Inactive, Active


class RoomType(db.Model, SerializerMixin):
    """ RoomsTypes model class"""

    __tablename__ = "room_type"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150), nullable=False)


# Schedule models
class Schedule(db.Model, SerializerMixin):
    """ Schedules model class"""

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String()) # Confirmed, Canceled, In_Progress, Concluded
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True)
    room_id = db.Column(db.Integer(), db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', lazy=True)
    created_at = db.Column(db.DateTime(), default=datetime.now(tz))
    updated_at = db.Column(db.DateTime(), default=datetime.now(tz))

    @override
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'status': self.status,
            'user': self.user.to_dict(),
            'room': self.room.to_dict(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
