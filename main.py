from flask import (
    Flask,
    request,
    redirect,
    make_response,
    render_template,
    session,
    url_for,
    flash
)

import unittest

from app import create_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from flask_login import login_required, current_user
from services.firestore_service import *

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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()

    ctx = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form,
        'update_form': update_form
    }

    if todo_form.validate_on_submit():
        description = todo_form.description.data

        create_todo(username, description)

        flash('Tarea Creada con éxito')

        return redirect(url_for('hello'))

    return render_template('hello.html', **ctx)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id, todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id, todo_id, done)

    return redirect(url_for('hello'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', error=error)
