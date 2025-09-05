from flask import g
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

from helpers.application import app


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)
cache = Cache(app)
