from data import db_session
from flask import Flask
from data import functions
from data import get_user_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'TipoVikipedia'


def main():
    db_session.global_init("db/sleep.db")
    app.register_blueprint(get_user_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
