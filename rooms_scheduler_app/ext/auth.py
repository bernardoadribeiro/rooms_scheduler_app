from flask import abort
from flask_simplelogin import SimpleLogin
from werkzeug.security import check_password_hash, generate_password_hash
from rooms_scheduler_app.ext.database import db, User


def verify_login(user):
    """Valida o usuario e senha para efetuar o login"""
    username = user.get('username')
    password = user.get('password')
    
    if not username or not password:
        return False
    
    existing_user = User.query.filter_by(username=username).first()
    if not existing_user:
        return False
    
    if check_password_hash(existing_user.password, password):
        return True
    return False


def create_user(username, password):
    """Registra um novo usuario caso nao esteja cadastrado"""
    if User.query.filter_by(username=username).first():
        abort(400, f'The user \'{username}\' already exists.')

    user = User(username=username, password=generate_password_hash(password))

    db.session.add(user)
    db.session.commit()
    
    return user


def init_app(app):
    SimpleLogin(app, login_checker=verify_login)