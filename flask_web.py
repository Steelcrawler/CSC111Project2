import os
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hi Tara! <h1>Hello World!<h1>'

@app.route('/<name>')
def user(name):
    return f'Hello {name}!'

@app.route('/admin/')
def admin():
    return redirect(url_for('user', name='Admin!'))

if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))
