from . import users
from . import stories
from . import db_session


def make_new_user(data: dict) -> str:
    """Функция для создания нового пользователя"""

    new_user = users.Users()
    new_user.id = data['id']
    new_user.name = data['name']
    new_user.login = data['login']
    new_user.hashed_password = data['hashed_password']
    new_user.own_stories = data['own_stories']
    db_sess = db_session.create_session()
    db_sess.add(new_user)
    try:
        db_sess.commit()
    except Exception as e:
        return f'Ошибка: {e}'
    else:
        return 'Удачно'


def make_new_story(data: dict) -> str:
    """Функция для добавления истории"""

    new_story = stories.Stories()
    new_story.id = data['id']
    new_story.name = data['name']
    new_story.text = data['text']
    db_sess = db_session.create_session()
    db_sess.add(new_story)
    user = db_sess.query(users.Users).filter(users.Users.id == data['user_id']).first()
    user.own_stories = user.own_stories + f', {data["id"]}'
    try:
        db_sess.commit()
    except Exception as e:
        return f'Ошибка: {e}'
    else:
        return 'Удачно'


def logining(data: dict):
    """По логину находит пользователя и даёт зайти на аккаунт если введён верный пароль"""

    db_sess = db_session.create_session()
    user = db_sess.query(users.Users).filter(users.Users.login == data['login']).first()
    if not user:
        return 'Неверный логин'
    if data['hashed_password'] == user.hashed_password:
        return {'name': user.name, 'own_stories': user.own_stories.split(', ')}
    else:
        return 'Введён неверный пароль'


def reading(sleep_id: dict):
    """Возможность читать историю по id"""

    db_sess = db_session.create_session()
    story = db_sess.query(stories.Stories).filter(stories.Stories.id == sleep_id).first()
    if not story:
        return 'Неверный ID'
    return {'name': story.name, 'text': story.text}
