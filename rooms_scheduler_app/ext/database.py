from typing_extensions import override

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


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
    info_lab = db.Column(db.Boolean())
    sciente_lab = db.Column(db.Boolean())
    classroom = db.Column(db.Boolean())


#  Room models
class Room(db.Model, SerializerMixin):
    """ Rooms model class"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'),
        nullable=False)
    type = db.relationship('RoomType', lazy=True)
    key_status = db.Column(db.String()) # Losed, On_Hand, Scheduled
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
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
