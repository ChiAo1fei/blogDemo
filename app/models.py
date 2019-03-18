"""__author__ == ChiAo"""
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# 生成数据访问对象
db = SQLAlchemy()


class Admin(db.Model):

    # 定义id主键，自增字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 管理员账号
    admin_id = db.Column(db.String(10), unique=True, nullable=False)

    # 管理员密码
    admin_pwd = db.Column(db.String(20), nullable=False)

    # 添加用户 或者用户修改信息
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 删除用户
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ArticleType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_name = db.Column(db.String(10), unique=True, nullable=False)
    arts = db.relationship('Article', backref='tp')

    __tablename__ = 'art_type'


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(10), unique=True, nullable=False)
    desc = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    type = db.Column(db.Integer, db.ForeignKey('art_type.id'))

