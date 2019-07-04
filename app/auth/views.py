from . import auth
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    session
)
from app.forms import LoginForm
from services.firestore_service import get_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        session['username'] = login_form.username.data

        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(user_id=username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if password == password_from_db:
                pass

        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('login.html', **context)
