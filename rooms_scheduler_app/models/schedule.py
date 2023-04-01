from ..ext.database import db, tz

from datetime import datetime
from typing_extensions import override

from sqlalchemy_serializer import SerializerMixin


class Schedule(db.Model, SerializerMixin):
    """ Schedules model class"""

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String())  # Confirmed, Canceled, In_Progress, Concluded
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
