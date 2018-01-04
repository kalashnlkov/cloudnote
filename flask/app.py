from flask import Flask, render_template, redirect, url_for, jsonify
from flask import request
import random
import SMSService

app = Flask(__name__)


@app.route("/editor")
def editor():
    return render_template('editor.html')


@app.route("/")
def index():
    # return redirect(url_for('editor'))
    return render_template('login.html')


@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    
    if  username == password:
        return redirect(url_for('editor'))
    return redirect(url_for('index'))

@app.route("/regist", methods=['POST','GET'])
def regist():
    print(request.form)
    print(request.method)
    if request.method == 'GET':
        print(url_for('regist'))
        return render_template('register.html')
    if request.method == 'POST':
        #TODO add db.
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        telephone = request.form['phone']
        print('username={} passowrd={}'.format(username,password1))
        # return redirect(url_for('index'))
    return u'error method'

#TODO send SMS code
@app.route("/sendSMS", methods=['POST'])
def sendSMS():
    print('-------sendSMS------')
    username = request.form['username']
    telephone = request.form['phone']
    verifycode = random.randint(100000,999999)
    SMSService.sendSms(str(telephone), str(verifycode))
    return jsonify({'status':'OK', 'username':username, 'phone':telephone})

@app.route("/agreement")
def agreement():
    return render_template('agreement.html')

if __name__ == "__main__":
    app.run(debug=True)
