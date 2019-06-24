from flask import (
    Flask,
    request,
    redirect,
    make_response,
    render_template
)
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


todos = range(5)


@app.route('/')
def index():
    ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('ip', ip)

    return response


@app.route('/hello')
def hello():
    ip = request.cookies.get('ip')

    ctx = {
        'user_ip': ip,
        'todos': todos
    }

    return render_template('hello.html', **ctx)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html', error=error)
