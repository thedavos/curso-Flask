from . import auth
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    session
)
from app.forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        session['username'] = login_form.username.data

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('login.html', **context)
