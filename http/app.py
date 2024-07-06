from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum

# load_dotenv('.env')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.before_request
def before_request():
    print('this is a before_request')
    # return 'this is a before_request'


@app.after_request
def after_request(response):
    print('this is a after_request')
    return response


@app.route('/')
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s!</h1>' % name
        if 'logged_in' in session:
            response += '[Authenticated]'
        else:
            response += '[Not Authenticated]'
        return response


@app.route('/goback/<int:year>')
def go_back(year: int):
    return '<p>Welcome to %d!</p>' % (2024 - year)


@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color: str):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


@app.route('/404')
def not_found():
    abort(404)


@app.route('/foo')
def foo():
    # data = {
    #     'name': 'zxb',
    #     'gender': 'male'
    # }
    # response = make_response(json.dumps(data))
    # response.mimetype = 'application/json'
    # return response
    return jsonify(name='zxb', gender='male')
    # return jsonify(message='Error!'), 500


@app.route('/json_error')
def json_error():
    return jsonify(message='Error!'), 500


@app.route('/set/<name>')
def set_cookie(name: str):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


@app.route('/login')
def login():
    session['logged_in'] = True
    return redirect(url_for('hello'))


@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page.'


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


@app.route('/hoo')
def hoo():
    return '<h1>Hoo page</h1><a href="%s">Do something and redirect</a>' % url_for(
        'do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' % url_for(
        'do_something', next=request.full_path)


@app.route('/do_something')
def do_something():
    return redirect_back()


# ajax发送异步信息
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
    <h1>A very long post</h1>
    <div class="body">%s</div>
    <button id="load">Load More</button>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $('#load').click(function() {
            $.ajax({
                url: '/more',
                type: 'get',
                success: function(data){
                    $('.body').append(data);
                }
            })
        })
    })
    </script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)