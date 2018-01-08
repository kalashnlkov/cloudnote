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
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('editor'))
        return render_template('login.html')
    user = User(username=request.form['username'],
                password=request.form['password'])
    if user.login()['status']:
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

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    usersession = request.cookies['session']
    print(usersession)
    session.pop(usersession, None)
    return redirect(url_for('index'))

@app.route("/user/update", methods=['POST', 'GET'])
def update():
    if request.method == 'GET':
        return render_template('forget_passwd.html')
    username = request.form['username']
    telephone = request.form['phone']
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 != password2:
        return jsonify({'status':'FAIL', 'message':'password dismatch'})
    user = User(username,telephone,password)
    ret = user.update()
    if ret['status']:
        return jsonify({'status':'SUCCESS', 'message':'password change success'})
    return jsonify({'status':'FAIL', 'message':'password change failed'})
    
@app.route("/agreement")
def agreement():
    return render_template('agreement.html')

app.secret_key = os.urandom(12)
if __name__ == "__main__":
    app.run(debug=True)
