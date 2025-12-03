from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:123456@postgres2025.1:5432/censo_escolar"
app.config['CACHE_TYPE'] = "RedisCache"
app.config['CACHE_REDIS_URL'] = 'redis://redis-temporario:6379/0'

api = Api(app)