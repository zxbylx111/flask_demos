from flask import Flask, render_template, Markup

app = Flask(__name__)
# 修改jinja变量界定符，原来是{{ }}，现在改为[[ ]]
# app.jinja_env.variable_start_string = '[['
# app.jinja_env.variable_end_string = ']]'

user = {
    'username': 'zxb',
    'bio': 'A boy who loves movies and music.'
}
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


# 注册模板上下文处理函数
@app.context_processor
def inject_foo():
    foo = 'I am foo.'
    return dict(foo=foo)


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


@app.route('/')
def index():
    return '<h1>hello flask</h1>'


# 注册模板全局函数
@app.template_global()
def bar():
    return 'I am bar.'


# 注册自定义过滤器
@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')


# 自定义测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    else:
        return False



