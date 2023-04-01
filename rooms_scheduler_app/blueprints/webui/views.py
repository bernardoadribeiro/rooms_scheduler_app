from flask import abort, render_template
from rooms_scheduler_app.ext.database import Schedule


def index():
    schedules = Schedule.query.all()
    return render_template("index.html", schedules=schedules)


def schedule(schedule_id):
    schedule = Schedule.query.filter_by(id=schedule_id).first() or abort(
        404, "produto nao encontrado"
    )
    return render_template("schedule.html", schedule=schedule)
