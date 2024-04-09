from flask import render_template, request, redirect, session
from data import db_session
from flask import Flask
from data import functions
from data import get_user_api
from data import users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TipoVikipedia'


@app.route('/', methods=['GET', 'POST'])
def home():
    session['username'] = ''
    if request.method == 'GET':
        return render_template('base.html', buttons=True, title='Sleeper')
    return redirect(f'/sleeps/{request.form["story_id"]}')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', buttons=False, message='', title='Авторизация')
    login, hashed_password = request.form['login'], functions.hashing_password(request.form['password'])
    db_sess = db_session.create_session()
    user = db_sess.query(users.Users).filter(users.Users.login == login).first()
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
    user = db_sess.query(users.Users).filter(users.Users.login == login).first()
    if user:
        return render_template('register.html', buttons=False, message='Такой логин уже используют',
                               title='Регистрация')
    user = db_sess.query(users.Users).filter(users.Users.name == name).first()
    if user:
        return render_template('register.html', buttons=False, message='Такое прозвище уже существует',
                               title='Регистрация')
    making = functions.make_new_user({'login': login, 'name': name, 'password': pasword})
    if making[0] != 'Удачно':
        return render_template('register.html', buttons=False, message=making, title='Регистрация')
    session['username'] = making[1].name
    return redirect(f'/my_wall/{making[1].name}')


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
    if request.method == 'GET':
        return render_template('base.html', buttons=False, message='', title=f'Страница {user}')



def main():
    db_session.global_init("db/sleep.db")
    app.register_blueprint(get_user_api.blueprint)
    app.run(debug=True)


if __name__ == '__main__':
    main()
