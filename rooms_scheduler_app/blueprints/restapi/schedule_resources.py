from datetime import datetime

from flask import jsonify, abort, request
from flask_restful import Resource
from rooms_scheduler_app.ext.database import (User, UserRoomPermission,
                                              Room, Schedule)

from ...ext.database import db, tz
from .helper import check_room_availability, has_room_permission


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
        if check_room_availability(start_time=start_time, end_time=end_time, date=date, room_id=room_id):
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
        if check_room_availability(start_time=schedule.start_time, end_time=schedule.end_time, date=schedule.date, room_id=room_id):
            pass

        # Check if the user has permission to access the room
        user_permissions = UserRoomPermission.query.filter_by(
            user_id=user_id, 
            room_type_id=Room.query.get(room_id).room_type_id
        ).first()
        if not user_permissions:
            abort(400, "User does not have permission to access this room.")
        
        db.session.commit()

        return jsonify(schedule.to_dict())




class AccessRequestHandlerResource(Resource):
    """ Handler for access of a room.
        
        Verifies if the user is allowed to access the room and if he has scheduled the room at the moment of request.

        Timezone: UTC-3
    """

    def get(self, user_id, room_id):

        if has_room_permission(user_id, room_id):
            pass

        now = datetime.now(tz).time()
        today = datetime.now(tz).date()

        schedules = Schedule.query.filter_by(
            user_id=user_id, 
            room_id=room_id, 
            date=today
        ).all()

        for schedule in schedules:
            # If the user has some schedule today
            if now > schedule.start_time and now < schedule.end_time and schedule.status == 'Confirmed':
                return jsonify({
                    'access': True,
                    'message': 'You have access to this room.',
                    'start_time': str(schedule.start_time),
                    'end_time': str(schedule.end_time)
                })
        
        # If the user is not allowed to access this room or does not have a schedule
        return {
            'access': False, 
            'message': 'You do not have access to this room.',
            'start_time': '',
            'end_time': ''
        }, 400
        