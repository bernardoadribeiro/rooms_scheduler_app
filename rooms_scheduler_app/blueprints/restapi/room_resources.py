from datetime import datetime

from flask import jsonify, abort, request
from flask_restful import Resource
from rooms_scheduler_app.ext.database import Room, RoomType

from ...ext.database import db

# Rooms Resources
class RoomsResource(Resource):
    """ Rooms Resource to GET all rooms or POST a new room."""
    def get(self):
        rooms = Room.query.all() or abort(404, "No rooms found.")

        return jsonify({
            'rooms': [
                room.to_dict()
                for room in rooms
            ]}
        )

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, "No data received in the body.")

        name = data.get('name')
        number = data.get('number')
        room_type_id = data.get('room_type_id')
        key_status = data.get('key_status')
        room_status = data.get('room_status')

        room_type = RoomType.query.get(room_type_id)
        if not room_type:
            abort(400, "Invalid Room Type ID.")

        new_room = Room(
            name=name,
            number=number,
            room_type_id=room_type_id,
            key_status=key_status,
            room_status=room_status
        )

        db.session.add(new_room)
        db.session.commit()

        return jsonify(new_room.to_dict())

class RoomResource(Resource):
    """ Room resource to update with PATCH or GET a specific room."""

    def get(self, room_id):
        room = Room.query.get(room_id) or abort(404, "Room not found.")
        
        return jsonify(room.to_dict())

    def patch(self, room_id):
        room = Room.query.get(room_id) or abort(404, "Room not found.")

        data = request.get_json()
        if not data:
            abort(400, "No data received in the body.")

        name = data.get('name')
        number = data.get('number')
        room_type_id = data.get('room_type_id')
        key_status = data.get('key_status')
        room_status = data.get('room_status')

        if name:
            room.name = name
        
        if number:
            room.number = number

        if room_type_id:
            room_type = RoomType.query.get(room_type_id)
            if not room_type:
                abort(400, "Invalid Room Type ID.")
            room.room_type = room_type
        
        if key_status:
            room.key_status = key_status
        
        if room_status:
            room.room_status = room_status
        
        db.session.commit()

        return jsonify(room.to_dict())
