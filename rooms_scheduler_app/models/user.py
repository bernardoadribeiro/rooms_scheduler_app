from ..ext.database import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    """ Users model class"""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    username = db.Column(db.String(140))
    password = db.Column(db.String(512))
    type = db.Column(db.String()) # Admin, Teacher, Student


class UserRoomPermission(db.Model, SerializerMixin):
    """ Users Rooms Permissions Permissions class"""

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True)
    info_lab = db.Column(db.Boolean())
    sciente_lab = db.Column(db.Boolean())
    classroom = db.Column(db.Boolean())
