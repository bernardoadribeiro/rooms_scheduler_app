from flask import abort
from rooms_scheduler_app.ext.database import (UserRoomPermission,
                                              Room, Schedule)


def check_room_availability(end_time, start_time, date, room_id):
    """ Check the availability of a room in the given period."""

    schedules = Schedule.query.filter_by(date=date, room_id=room_id).all()

    # if there are any schedules in the given date
    if schedules:
        for schedule in schedules:
            # if the schedule is between a existing schedule
            if start_time >= schedule.start_time and end_time <= schedule.end_time:
                abort(
                    400, "The START and END of the schedule must be BEFORE or AFTER a existing schedule. Not in the middle of one.")

            # if the schedule ending is in the middle of a existing schedule
            if end_time >= schedule.start_time and end_time <= schedule.end_time:
                abort(
                    400, "The END time of the schedule must be BEFORE the BEGIN of a existing schedule.")

            # if the schedule begining is in the middle of a existing schedule
            if start_time >= schedule.start_time and start_time <= schedule.end_time:
                abort(
                    400, "The BEGIN time of the schedule must be AFTER the END of a existing schedule.")

            # if the schedule is 'holding' a existing schedule
            if start_time <= schedule.start_time and end_time >= schedule.end_time:
                abort(
                    400, "The START and END of the schedule must be BEFORE or AFTER a existing schedule. Not 'holding' one.")

            # if the schedule is ending before it starts
            if end_time <= start_time:
                abort(
                    400, "The END time must be greater than start time. The Schedule must end after it starts.")

    return True


def has_room_permission(user_id, room_id):
    """Check if the user has permission to access this type of room"""

    room = Room.query.filter_by(id=room_id).first()

    user_permission = UserRoomPermission.query.filter_by(
        user_id=user_id, room_type_id=room.room_type_id
    ).first()

    if not user_permission:
        # If the user is not allowed to access this room or does not have a schedule
        abort(400, {
            'access': False,
            'message': 'The user do not have access to this room.',
            'start_time': '',
            'end_time': ''
        })
    else:
        return True
