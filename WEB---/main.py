from data import db_session
from flask import Flask
from data import functions

# app = Flask(__name__)


def main():
    db_session.global_init("db/sleep.db")
    # app.run()


if __name__ == '__main__':
    main()