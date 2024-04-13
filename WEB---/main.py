from flask import render_template, request, redirect, session
from data import db_session
from flask import Flask
from data import functions
from data import get_user_api
from data.users import Users
from data.stories import Stories

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TipoVikipedia'


@app.route('/', methods=['GET', 'POST'])
def home():
    session['username'] = ''
    db_sess = db_session.create_session()
    sleeps = db_sess.query(Stories).all()
    if request.method == 'GET':
        return render_template('homepage.html', buttons=True, title='Sleeper', sleeps=sleeps)
    return redirect(f'/sleeps/{request.form["story_id"]}')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', buttons=False, message='', title='Авторизация')
    login, hashed_password = request.form['login'], functions.hashing_password(request.form['password'])
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.login == login).first()
    if not user:
        return render_template('login.html', buttons=False, message='Неверный логин', title='Авторизация')
    if user.hashed_password != hashed_password:
        return render_template('login.html', buttons=False, message='Неверный пароль', title='Авторизация')
    session['username'] = user.name
    return redirect(f'/my_wall/{user.name}')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', buttons=False, message='', title='Регистрация')
    login, name, pasword = request.form['login'], request.form['name'], request.form['password']
    if not all((login, name, pasword)):
        return render_template('regiser.html', buttons=False, message='Все поля должны быть заполнены',
                               title='Регистрация')
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.login == login).first()
    if user:
        return render_template('register.html', buttons=False, message='Такой логин уже используют',
                               title='Регистрация')
    user = db_sess.query(Users).filter(Users.name == name).first()
    if user:
        return render_template('register.html', buttons=False, message='Такое прозвище уже существует',
                               title='Регистрация')
    making = functions.make_new_user({'login': login, 'name': name, 'password': pasword})
    if making[0] != 'Удачно':
        return render_template('register.html', buttons=False, message=making, title='Регистрация')
    session['username'] = making[1]
    return redirect(f'/my_wall/{making[1]}')


@app.route('/sleeps/<id>', methods=['GET'])
def sleep(id):
    try:
        id = int(id)
    except Exception:
        return render_template('read_story.html', message='Ошибка при вводе id', buttons=False, title='Ошибка id')
    answer = functions.reading(id)
    if answer == 'Неверный ID':
        return render_template('read_story.html', name='Такой истории не существует', text='', buttons=False,
                               title='Несуществующая история')
    return render_template('read_story.html', name=answer['name'], text=answer['text'], buttons=False,
                           title=f'История №{id}')


@app.route('/my_wall/<user>', methods=['GET', 'POST'])
def show(user):
    if user not in session['username']:
        return redirect('/')
    db_sess = db_session.create_session()
    sleeps = db_sess.query(Stories).all()
    maks = max((sleep.id for sleep in sleeps))
    cur_user = db_sess.query(Users).filter(Users.name == str(user)).first()
    leest = cur_user.own_stories.split(', ')
    stories = [story for story in sleeps if str(story.id) in leest]
    if request.method == 'GET':
        return render_template('userpage.html', buttons=False, message='', title=f'Страница {user}', sleeps=stories)
    if all([request.form['name'], request.form['text']]):
        return render_template('userpage.html', buttons=False, message=functions.make_new_story(
            {'name': request.form['name'], 'text': request.form['text'], 'user_id': cur_user.id, 'id': maks + 1}),
                               title=f'Страница {user}', sleeps=stories)
    return render_template('userpage.html', buttons=False, message='Нужно заполнить все поля', title=f'Страница {user}',
                           sleeps=stories)


def main():
    db_session.global_init("db/sleep.db")
    app.register_blueprint(get_user_api.blueprint)
    app.run(debug=True)


if __name__ == '__main__':
    main()
