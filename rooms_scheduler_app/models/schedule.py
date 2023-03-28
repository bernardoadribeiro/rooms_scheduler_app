from ..ext.database import db
from sqlalchemy_serializer import SerializerMixin

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
