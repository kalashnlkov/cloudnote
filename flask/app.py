from flask import Flask, render_template, redirect, url_for
from flask import request

app = Flask(__name__)


@app.route("/editor")
def editor():
    return render_template('editor.html')


@app.route("/")
def index():
    # return redirect(url_for('editor'))
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    
    if  username == password:
        return redirect(url_for('editor'))
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()