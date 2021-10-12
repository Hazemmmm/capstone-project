
import os
from sqlalchemy import (
    Column,
    String,
    Integer,
    create_engine,
    Date
)
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from dataclasses import dataclass

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'capstone')
# DB_PATH = 'postgres://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
DB_PATH = 'postgres://lulfqpegtegxij:e0135146ffc824e92355d323a9bf4d69a7d3605301334c907d2279089faee986@ec2-54-208-96-16.compute-1.amazonaws.com:5432/dd87refgtcrif7'
# DB_PATH = os.environ.get('DATABASE_URL')
SQLALCHEMY_DATABASE_URI = DB_PATH

db = SQLAlchemy()


def setup_db(app, database_path=DB_PATH):
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


class inheritanceCRUDOperation(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


@dataclass
class Movie(inheritanceCRUDOperation):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


@dataclass
class Actor(inheritanceCRUDOperation):

    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):

        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
