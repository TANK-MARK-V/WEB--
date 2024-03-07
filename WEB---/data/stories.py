import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Stories(SqlAlchemyBase):
    __tablename__ = 'stories'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.TEXT)
