from flask import Flask, render_template, request, session
from models.user import User
from common.database import Database

app = Flask(__name__)
app.secret_key = "aayush"


@app.route('/')
def hello_world():
    return render_template('login.html')


@app.before_first_request
def database_initialize():
    Database.initialize()


@app.route('/login', methods=['POST'])
def login_page():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password) is True:
        User.login(email)
        return render_template('profile.html', email=session['email'])


if __name__ == '__main__':
    app.run()

