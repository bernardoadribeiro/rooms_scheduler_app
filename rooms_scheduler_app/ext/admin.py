from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib import sqla
from flask_simplelogin import login_required
from werkzeug.security import generate_password_hash

from rooms_scheduler_app.ext.database import db, Room, RoomType, User, UserRoomPermission, Schedule

# Proteger o admin com login via Monkey Patch
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
sqla.ModelView._handle_view = login_required(sqla.ModelView._handle_view)
admin = Admin()


class UserAdmin(sqla.ModelView):
    column_list = ['username']
    can_edit = False

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password)


def init_app(app):
    admin.name = app.config.TITLE
    admin.template_mode = app.config.FLASK_ADMIN_TEMPLATE_MODE
    admin.init_app(app)
    admin.add_view(sqla.ModelView(Room, db.session))
    admin.add_view(sqla.ModelView(RoomType, db.session))
    admin.add_view(sqla.ModelView(Schedule, db.session))
    admin.add_view(sqla.ModelView(UserRoomPermission, db.session))
    admin.add_view(UserAdmin(User, db.session))
