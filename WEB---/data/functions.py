from . import users
from . import stories
from . import db_session


def make_new_user(data: dict) -> str:
    """Функция для создания нового пользователя"""

    new_user = users.Users()
    new_user.name = data['name']
    new_user.login = data['login']
    new_user.hashed_password = hashing_password(data['hashed_password'])
    new_user.own_stories = ''
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


def hashing_password(old_password: str) -> str:
    alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    nums = '0123456789'
    ind = 0
    for letter in old_password.lower()[::-1]:
        if letter in alph:
            ind = alph.index(letter)
            break
        elif letter in alphabet:
            ind = alphabet.index(letter)
            break
        elif letter in nums:
            ind = int(letter)
            break
    password = ''
    for i in range(len(old_password[::-1])):
        letter = old_password[::-1][i].lower()
        if letter in alph:
            password += alph[(alph.index(letter) + ind % len(alph))]
        elif letter in alphabet:
            password += alphabet[(alphabet.index(letter) + ind % len(alphabet))]
        elif letter in nums:
            password += nums[(nums.index(letter) + ind % len(nums))]
    return password
