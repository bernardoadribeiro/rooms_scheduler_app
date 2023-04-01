from flask import Blueprint
from .views import index, schedule

bp = Blueprint("webui", __name__, template_folder="templates",
               url_prefix="/"
               )

bp.add_url_rule('/', view_func=index)
bp.add_url_rule('/main/v1', view_func=index)
bp.add_url_rule(
    "/main/v1/schedules/<schedule_id>", view_func=schedule, endpoint="scheduleview"
)


def init_app(app):
    app.register_blueprint(bp)
