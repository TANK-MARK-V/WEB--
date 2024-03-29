from flask import Blueprint, jsonify, request
from .users import Users
from . import db_session
from .functions import make_new_user
from .functions import hashing_password

blueprint = Blueprint('news_api', __name__, template_folder='templates')


@blueprint.route('/api/add_user/<options>')
def add_user(options):
    key, name, login, password = options.split('&')
    if key != 'making':
        return 'Неверно введён код'
    return make_new_user({'name': name, 'login': login, 'hashed_password': hashing_password(password)})


@blueprint.route('/api/delete_user/<options>')
def delete_user(options):
    key, user_id = options.split('&')
    if key != 'udovletvorenie':
        return 'Неверно введён код'
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == int(user_id)).first()
    db_sess.delete(user)
    db_sess.commit()
    return 'Удачно'


@blueprint.route('/api/get_user/<options>')
def get_user(options):
    key, user_id = options.split('&')
    if key != 'udovletvorenie':
        return 'Неверно введён код'
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.id == int(user_id)).first()
    return jsonify(
        {
            'user':
                [user.to_dict(only=('name', 'own_stories'))]
        }
    )


@blueprint.route('/api/get_users/<options>')
def get_users(options):
    key = options
    if key != 'udovletvorenie':
        return 'Неверно введён код'
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'own_stories')) for item in users]
        }
    )
