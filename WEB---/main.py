from flask import render_template, request, redirect
from flask_login import login_user

from data import db_session
from flask import Flask
from data import functions
from data import get_user_api
from data import users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TipoVikipedia'


@app.route('/')
def home():
    return render_template('base.html', buttons=True)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', buttons=False, message='')
    login, hashed_password = request.form['login'], functions.hashing_password(request.form['password'])
    db_sess = db_session.create_session()
    user = db_sess.query(users.Users).filter(users.Users.login == login).first()
    if not user:
        return render_template('login.html', buttons=False, message='Неверный логин')
    if user.hashed_password != hashed_password:
        return render_template('login.html', buttons=False, message='Неверный пароль')
    return redirect('/my_wall')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', buttons=False, message='')
    login, name, pasword = request.form['login'], request.form['name'], request.form['password']
    if not all((login, name, pasword)):
        return render_template('regiser.html', buttons=False, message='Все поля должны быть заполнены')
    db_sess = db_session.create_session()
    user = db_sess.query(users.Users).filter(users.Users.login == login).first()
    if user:
        return render_template('register.html', buttons=False, message='Такой логин уже используют')
    user = db_sess.query(users.Users).filter(users.Users.name == name).first()
    if user:
        return render_template('register.html', buttons=False, message='Такое прозвище уже существует')
    making = functions.make_new_user({'login': login, 'name': name, 'password': pasword})
    if making != 'Удачно':
        return render_template('register.html', buttons=False, message=making)
    return redirect('/my_wall')


def main():
    db_session.global_init("db/sleep.db")
    app.register_blueprint(get_user_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
