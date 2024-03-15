from flask import Blueprint, jsonify
from .users import Users
from . import db_session

blueprint = Blueprint('news_api', __name__, template_folder='templates')


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
