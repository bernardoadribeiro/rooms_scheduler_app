from ..ext.database import db

from sqlalchemy_serializer import SerializerMixin


class Room(db.Model, SerializerMixin):
    """ Rooms model class"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'),
                             nullable=False)
    room_type = db.relationship('RoomType', lazy=True)
    key_status = db.Column(db.String())  # Lost, On_Hand, Scheduled
    room_status = db.Column(db.String())  # Inactive, Active


class RoomType(db.Model, SerializerMixin):
    """ RoomsTypes model class"""

    __tablename__ = "room_type"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150), nullable=False)
