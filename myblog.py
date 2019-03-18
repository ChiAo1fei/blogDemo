"""__author__ == ChiAo"""
import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from app.models import db
from app.views import blue
from web.views import web_blue

app = Flask(__name__)
app.register_blueprint(blueprint=blue, url_prefix='/back')
app.register_blueprint(blueprint=web_blue, url_prefix='/web')

app.secret_key = '123789'
# 配置session信息
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
Session(app)

# 配置数据库信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ChiAo1fei@localhost:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()
