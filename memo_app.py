from datetime import datetime
from importlib import import_module

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

try:
    Markdown = import_module("flask_markdown").Markdown
except ImportError:
    Markdown = None

app = Flask(__name__)
if Markdown is not None:
    Markdown(app)


db_uri = 'mysql+pymysql://root:1234@localhost/mylog?charset=utf8'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text())
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()


@app.route('/')
def list_posts():
    message = "メモ一覧"

    posts = Post.query.all()
    return render_template('list.html', message = message, posts = posts)



@app.route('/show/<int:id>')
def show_post(id):

    post = Post.query.get(id)

    return render_template('show.html', post = post)


@app.route('/new')
def new_post():

    return render_template('new.html')

@app.route('/create', methods=['post'])
def create_post():

    new_post = Post()
    new_post.title = request.form['title']
    new_post.content = request.form['content']
    db.session.add(new_post)
    db.session.commit()

    post = Post.query.get(new_post.id)

    return render_template('show.html', post = post)


@app.route('/destroy/<int:id>')
def destroy_post(id):
    message = "メモ一覧"

    destroy_post = Post.query.get(id)
    db.session.delete(destroy_post)
    db.session.commit()

    posts = Post.query.all()

    return render_template('list.html', message = message, posts = posts)



@app.route('/edit/<int:id>')
def edit_post(id):

    post = Post.query.get(id)

    return render_template('edit.html', post = post)


@app.route('/update/<int:id>', methods=['post'])
def update_post(id):

    update_post = Post.query.get(id)
    update_post.title = request.form['title']
    update_post.content = request.form['content']
    db.session.commit()

    post = Post.query.get(id)

    return render_template('show.html', post = post)
