from flask import render_template, redirect, session
from flask import url_for, request, jsonify
from flask import current_app as app
from flask_login import login_required
from werkzeug.security import generate_password_hash as GPH
from werkzeug.security import check_password_hash as CPH

from app.fronted import fronted
from app.models import *

import json
import os
import time

@fronted.route("/editor")
def editor():
    return render_template('editor.html')


@fronted.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('.editor'))
    return redirect(url_for('.login'))

@fronted.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('editor'))
        return render_template('login.html')
    user = User(name=request.form['username'],
                password=request.form['password'])
    if user.login()['status']:
        session['username'] = user.username
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@fronted.route("/regist", methods=['POST','GET'])
def regist():
    print(request.form)
    print(request.method)
    if request.method == 'GET':
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

@fronted.route("/sendSMS", methods=['POST'])
def sendSMS():
    username = request.form['username']
    telephone = request.form['phone']
    user = User(name=username,phone=telephone)
    status = 'FAIL'
    if user.regist():
        status = 'SUCCESS'
    return jsonify({'status':status, 'username':username, 'phone':telephone})

@fronted.route("/logout", methods=['POST', 'GET'])
def logout():
    usersession = request.cookies['session']
    print(usersession)
    session.pop(usersession, None)
    return redirect(url_for('index'))

 
@fronted.route("/user/update", methods=['POST', 'GET'])
def update():
    if request.method == 'GET':
        return render_template('forget_passwd.html')
    username = request.form['username']
    telephone = request.form['phone']
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 != password2:
        return jsonify({'status':'FAIL', 'message':'password dismatch'})
    user = User(username,telephone,password1)
    ret = user.update()
    if ret['status']:
        return jsonify({'status':'SUCCESS', 'message':'password change success'})
    return jsonify({'status':'FAIL', 'message':'password change failed'})

@fronted.route("/note/new", methods=['POST'])
def new_note():
    #TODO auth check. maybe check session.
    note_name = request.form['notename']
    note_content = request.form['notecontent']
    note = Note(note_name,note_content,session['username'])
    ret = note.insert()
    if ret['status']:
        return jsonify({'status':'SUCCESS', 'message':'note insert success'})
    return jsonify({'status':'FAIL', 'message':ret['message']})

@fronted.route("/agreement")
def agreement():
    return render_template('agreement.html')

@fronted.route("/file/upload", methods=['POST'])
def upload():
    """view to handle upload file
    """
    file = request.files.get("file_data")
    msg = api_upload(file)
    upload_msg = json.loads(msg.data.decode('utf-8'))
    message = upload_msg.get('url')
    return jsonify({'status':'SUCCESS', 'filename':message})

@fronted.route("/pdf", methods=['GET'])
def pdf():
    return render_template("pdf.html")

def api_upload(file):
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_dir = os.path.join(basedir,app.config['UPLOAD_FOLDER'])
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    fname = file.filename
    suffix = fname.rsplit('.',1)[1]
    int_time = int(time.time())
    new_name = '%s.%s'%(int_time, suffix)
    file.save(os.path.join(file_dir, new_name))
    print(os.path.join(file_dir, new_name))
    url = url_for('fronted.static',filename="doc/%s"%(new_name),_external=True)
    print(url)
    print(url)
    #TODO convert to pdf if not pdf file
    return jsonify({'statys':'SUCCESS', 'message':new_name, 'url':url})
