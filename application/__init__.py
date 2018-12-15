from __future__ import with_statement
from contextlib import closing
from flask import Flask, url_for, request, render_template, session, redirect, escape, g, flash, abort, _app_ctx_stack
import sqlite3
from .db_server import *

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def index():
    return redirect(url_for('board'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(username)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/board')
def board():
    res = connection('/board/list')
    board_list = get_json(res)
    return render_template('board.html', board_list=board_list)

@app.route('/article/')
@app.route('/article/<id>')
def article(id):
    target = '/board/article/' + str(id)
    res = connection(target)
    article = get_json(res)
    return render_template('article.html', article=article) + article['body']

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

# set the secret key. keep this really secret:
app.secret_key = 'AOZr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(host='')
