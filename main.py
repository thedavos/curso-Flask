from flask import (
    Flask,
    request,
    redirect,
    make_response,
    render_template,
    session,
    url_for,
)

import unittest

from app import create_app
from flask_login import login_required
from services.firestore_service import get_users, get_todos

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello')
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    ctx = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    return render_template('hello.html', **ctx)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', error=error)
