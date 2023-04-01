from ..ext.database import db

from typing_extensions import override
from sqlalchemy_serializer import SerializerMixin


class User(db.Model, SerializerMixin):
    """ Users model class"""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    type = db.Column(db.String())  # Admin, Teacher, Student

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
