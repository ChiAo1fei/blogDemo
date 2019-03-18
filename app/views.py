"""__author__ == ChiAo"""


# 注册
from flask import request, render_template, Blueprint, session, \
    redirect, url_for

from app.models import db, Admin, Article, ArticleType
from utils.functions import is_login


blue = Blueprint('first', __name__)


@blue.route('/register/', methods=['POST', 'GET'])
def register():

    # 迁移模型
    db.create_all()

    # 渲染页面
    if request.method == 'GET':
        return render_template('backend/register.html')

    # 页面逻辑
    if request.method == 'POST':
        # request
        # 获取注册的信息
        username = request.form.get('username')
        password = request.form.get('password1')
        password2 = request.form.get('password2')

        # 判断用户输入的用户名是否已经存在或者两次密码是否不相等，
        admin_id = Admin.query.filter_by(admin_id=username).first()
        if admin_id is None and password2 == password:

            admin = Admin()
            admin.admin_id = username
            admin.admin_pwd = password

            admin.save()
            return redirect(url_for('first.login'))
        else:
            error = '信息不正确'
            return render_template('backend/register.html', error=error)
        # 判断注册信息
        # if username == 'ChiAo1fei' and password == '123456' and password == password2:
        #     # return render_template('backend/login.html')
        #     return redirect(url_for('first.login'))
        # else:
        #     return render_template('backend/register.html')


# 登录
@blue.route('/login/', methods=['GET', 'POST'])
def login():
    # 渲染页面
    if request.method == 'GET':
        return render_template('backend/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 用户输入账号后判断是否存在或者密码是否正确
        # 从数据库库中查询到相关信息
        admin = Admin.query.filter_by(admin_id=username).first()
        if admin is not None:
            if admin.admin_id == username and admin.admin_pwd == password:
                session['login_status'] = 1
                return redirect(url_for('first.index'))
            else:
                return render_template('backend/login.html')
        else:
            return render_template('backend/login.html')
        # # request
        # if username == 'ChiAo1fei' and password == '123456':
        #     session['login_status'] = 1
        #     # return render_template('backend/index.html')
        #     return redirect(url_for('first.index'))
        # else:
        #     return render_template('backend/login.html')


# 登录态
@blue.route('/index/')
@is_login
def index():
    return render_template('backend/index.html')


# 注销
@blue.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['login_status']
    return redirect(url_for('first.login'))


@blue.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()

        return render_template('backend/category_list.html', types=types)


@blue.route('/add_type/', methods=['GET','POST'])
def add_type():
    if request.method == 'GET':
        return render_template('backend/category_detail.html')

    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            # 保存分类信息
            art_type = ArticleType()
            art_type.t_name = atype

            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('first.a_type'))
        else:
            error = '请输入分类信息'
            return render_template('backend/category_detail.html', error=error)


@blue.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):
    # 删除分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()

    return redirect(url_for('first.a_type'))


@blue.route('/article_list/', methods=['GET'])
def article_list():
    articles = Article.query.all()
    return render_template('backend/article_list.html', articles=articles)


# 添加文章页面
@blue.route('/article_detail/', methods=['POST', 'GET'])
def article_detail():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('/backend/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            # 保存
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('first.article_list'))
        else:
            error = '请填写完整的文章信息'
            return render_template('backend/article_detail.html')