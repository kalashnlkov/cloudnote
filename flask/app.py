import json
import sys
import os
from flask import Flask, render_template, redirect, url_for, jsonify
from flask import request, session
from db.User import User

app = Flask(__name__)


@app.route("/editor")
def editor():
    return render_template('editor.html')


@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('editor'))
    return redirect(url_for('login'))


@app.route("/login", methods=['POST','GET'])
def login():
    if 'username' in session:
        return redirect(url_for('editor'))
    if request.method == 'GET':
        return render_template('login.html')
    user = User(username=request.form['username'],
                password=request.form['password'])
    if user.login():
        session['username'] = user.username
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route("/regist", methods=['POST','GET'])
def regist():
    print(request.form)
    print(request.method)
    if request.method == 'GET':
        print(url_for('regist'))
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        telephone = request.form['phone']
        verifycode = request.form['verifycode']
        if password1 != password2:
            return u'password dismatch'
        user = User(str(username), str(telephone), str(password1))
        user.verifycode = verifycode
        ret = user.insert()
        ret = json.loads(ret)
        if ret['status']:
            return redirect(url_for('login'))
        return jsonify(ret)
        # return redirect(url_for('index'))
    return u'error method'

@app.route("/sendSMS", methods=['POST'])
def sendSMS():
    username = request.form['username']
    telephone = request.form['phone']
    user = User(username, telephone)
    status = 'FAIL'
    if user.regist():
        status = 'SUCCESS'
    return jsonify({'status':status, 'username':username, 'phone':telephone})

@app.route("/logout", methods=['POST'])
def logout():
    usersession = request.cookies.get['session']
    print(usersession)
    session.pop(usersession, None)

@app.route("/agreement")
def agreement():
    return render_template('agreement.html')

app.secret_key = os.urandom(12)
if __name__ == "__main__":
    app.run(debug=True)
