from datetime import datetime

from flask import jsonify, abort, request
from flask_restful import Resource
from rooms_scheduler_app.ext.database import (User, UserRoomPermission,
                                              Room, RoomType, Schedule)

from ...ext.database import db, tz
from ...ext.auth import create_user


# APIs Resources

# Users Resources
class UsersResource(Resource):
    """ Users Resource"""
    def get(self):
        users = User.query.all() or abort(204)

        return jsonify(
            {'users':[ 
                user.to_dict()
                for user in users
            ]}
        )

    def post(self):
        data = request.get_json()
        if not data:
            abort(400, "No data received in the body.")

        username = data.get('username')
        password = data.get('password')

        new_user = create_user(username, password)

        return jsonify(new_user.to_dict())

class UserResource(Resource):
    """ User resource. Returns a single user."""
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first() or abort(404)
        
        return jsonify(user.to_dict())
    

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


# Schedule Resources
class SchedulesResource(Resource):
    """ Schedules Resource to GET all schedules or POST a new schedule."""
    def get(self):
        """ GET all schedules """
        schedules = Schedule.query.all() or abort(404, "No schedules found.")

        return jsonify({
            'schedules': [
                schedule.to_dict()
                for schedule in schedules   
            ]}
        )

    def post(self):
        """ POST a new schedule """
        data = request.get_json()
        if not data: 
            abort(400, "No data received in the body.")

        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        status = data.get('status')
        user_id = data.get('user_id')
        room_id = data.get('room_id')
        created_at = datetime.now(tz)
        updated_at = datetime.now(tz)

        date=datetime.strptime(date, "%Y-%m-%d").date()
        start_time=datetime.strptime(start_time, "%H:%M:%S").time()
        end_time=datetime.strptime(end_time, "%H:%M:%S").time()

        user = User.query.get(user_id)
        if not user:
            abort(400, "Invalid User ID.")
        
        room = Room.query.get(room_id)
        if not room:
            abort(400, "Invalid Room ID.")

        # Checking if the selected period is available
        if check_room_availability(start_time=start_time, end_time=end_time, date=date):
            pass
       
        # Check if the user has permission to access the room
        user_permissions = UserRoomPermission.query.filter_by(
            user_id=user_id, room_type_id=room.room_type_id
        ).first()
        if not user_permissions:
            abort(400, "User does not have permission to access this room.")
        
        new_schedule = Schedule(
            date=date,
            start_time=start_time,
            end_time=end_time,
            status=status,
            user_id=user_id,
            room_id=room_id,
            created_at=created_at,
            updated_at=updated_at
        )

        db.session.add(new_schedule)
        db.session.commit()

        return jsonify(new_schedule.to_dict())

class ScheduleResource(Resource):
    """ Schedule resource to update with PATCH or GET a specific schedule."""

    def get(self, schedule_id):
        schedule = Schedule.query.get(schedule_id) or abort(404, "Schedule not found.")
        
        return jsonify(schedule.to_dict())

    def patch(self, schedule_id):
        schedule = Schedule.query.get(schedule_id) or abort(404, "Schedule not found.")

        data = request.get_json()
        if not data:
            abort(400, "No data received in the body.")

        date = data.get('date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        status = data.get('status')
        user_id = data.get('user_id')
        room_id = data.get('room_id')

        schedule.updated_at = datetime.now(tz)

        if date:
            schedule.date = datetime.strptime(date, "%Y-%m-%d").date()
        
        if start_time:
            schedule.start_time = datetime.strptime(start_time, "%H:%M:%S").time()
        
        if end_time:
            schedule.end_time = datetime.strptime(end_time, "%H:%M:%S").time()

        if status:
            schedule.status = status
            
        if user_id:
            user = User.query.get(user_id)
            if not user:
                abort(400, "Invalid User ID.")
            schedule.user_id = user_id
        
        if room_id:
            room = Room.query.get(room_id)
            if not room:
                abort(400, "Invalid Room ID.")
            schedule.room_id = room_id

        # Checking if the selected period is available
        if check_room_availability(start_time=schedule.start_time, end_time=schedule.end_time, date=schedule.date):
            pass

        # Check if the user has permission to access the room
        user_permissions = UserRoomPermission.query.filter_by(
            user_id=user_id, room_type_id=room.room_type_id
        ).first()
        if not user_permissions:
            abort(400, "User does not have permission to access this room.")
        
        db.session.commit()

        return jsonify(schedule.to_dict())


def check_room_availability(end_time, start_time, date):
    """ Check the availability of a room in the given period."""

    schedules = Schedule.query.filter_by(date=date).all()

    # if there are any schedules in the given date
    if schedules:
        for schedule in schedules:
            # if the schedule is between a existing schedule
            if start_time >= schedule.start_time and end_time <= schedule.end_time:
                abort(400, "The START and END of the schedule must be BEFORE or AFTER a existing schedule. Not in the middle of one.")

            # if the schedule ending is in the middle of a existing schedule
            if end_time >= schedule.start_time and end_time <= schedule.end_time:
                abort(400, "The END time of the schedule must be BEFORE the BEGIN of a existing schedule.")
            
            # if the schedule begining is in the middle of a existing schedule
            if start_time >= schedule.start_time and start_time <= schedule.end_time:
                abort(400, "The BEGIN time of the schedule must be AFTER the END of a existing schedule.")

            # if the schedule is 'holding' a existing schedule
            if start_time <= schedule.start_time and end_time >= schedule.end_time:
                abort(400, "The START and END of the schedule must be BEFORE or AFTER a existing schedule. Not 'holding' one.")

            # if the schedule is ending before it starts
            if end_time <= start_time:
                abort(400, "The END time must be greater than start time. The Schedule must end after it starts.")
    
    return True
