from flask import Blueprint, render_template, request, redirect, url_for

from app.models import Article, ArticleType

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        articles = Article.query.all()
        types = ArticleType.query.all()
        return render_template('frontend/index.html', articles=articles, types=types)

    if request.method == 'POST':
        keyboard = request.form.get('keyboard')
        articles = Article.query.filter(Article.title.like('%'+keyboard+'%')).all()
        return render_template('frontend/share.html', articles=articles)


@web_blue.route('/info/<int:id>/', methods=['GET', 'POST'])
def info(id):
    article = Article.query.get(id)
    if id != 1:
        i = 1
        last_article = Article.query.get(id - i)
        while last_article is None:
            i = i + 1
            last_article = Article.query.get(id - i)
        last_title = last_article.title
        last_id = last_article.id
    else:
        last_title = '返回首页'
        last_id = None

    articles = Article.query.all()
    if id < len(articles):
        i = 1
        next_article = Article.query.get(id + i)
        while next_article is None:
            i = i + 1
            next_article = Article.query.get(id + i)
        next_title = next_article.title
        next_id = next_article.id
    else:
        next_title = '返回首页'
        next_id = None

    return render_template('frontend/info.html', article=article, last_title=last_title, next_title=next_title,
                           last_id=last_id, next_id=next_id)


@web_blue.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('frontend/about.html')


@web_blue.route('/gbook/', methods=['GET', 'POST'])
def gbook():
    return render_template('frontend/gbook.html')


@web_blue.route('/list/<string:type>/', methods=['GET', 'POST'])
def art_list(type):
    # print(type)
    art_type = ArticleType.query.filter(ArticleType.t_name == type).first()
    print(art_type.id)
    articles = Article.query.filter(Article.type == art_type.id).all()
    return render_template('frontend/list.html', articles=articles)


@web_blue.route('/share/', methods=['GET', 'POST'])
def share():
    return render_template('frontend/share.html')