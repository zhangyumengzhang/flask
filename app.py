import subprocess
from datetime import datetime
import os
import wave
from typing import cast

from flask import Flask, request, jsonify
import pymysql
from soundfile import read
from sqlalchemy.sql.elements import Null

from init import db, app
from model.User import User
from model.audioInfo import audioinfo

#登录
@app.route('/login', methods=['post'])
def login():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    sql = " select password from user where username='" +username+ "'";
    print(sql)
    ans = db.session.execute(sql)

    getpass = ans.fetchall()  # 获取所有数据
    getpass = getpass[0]
    if(getpass[0] == ''):
        data1 = {
            'status': '0',
            'message': '该账号不存在'
        }
    elif (getpass[0] == password):
        data1 = {
            'status': '1',
            'message': '登录成功'
         }
    else:
        data1 = {
            'status': '0',
            'message': '密码错误'
        }
    print(getpass[0])
    return data1

# 注册
@app.route('/register', methods=['post'])
def register():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']
    #用户名不能重复
    user = User.query.filter_by(username=username)
    print(user.count())
    if (user.count() != 0):
        data1 = {
            'status': '0',
            'message': '用户名已存在！'
        }
    else:
      try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        data1 = {
            'status': '1',
            'message': '注册成功！'
        }
      except(Exception):
        data1 = {
            'status': '0',
            'message': '注册失败！'
        }
    return data1

# 忘记密码
@app.route('/forget', methods=['post'])
def forget():
    data = request.get_json(silent=True)
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username)
    print(user.count())
    if(user.count() == 0):
        data1={
            'status': '0',
            'message': '没有该用户名！'
        }
    else:
     try:
        sql = " update user set password ='" + password + "'" + " where username='" + username + "'";
        print(sql)
        db.session.execute(sql)
        db.session.commit()
        data1 = {
            'status': '1',
            'message': '密码修改成功'
        }
     except (Exception):
        data1 = {
            'status': '0',
            'message': '密码修改失败'
        }
    return data1

#获取音频
@app.route('/getaudio', methods=['post'])
def getaudio():
    data = request.get_json(silent=True)
    username = data['username']
    sql = " select title,audiotime,isstar,type from audioinfo,user where audioinfo.userid = user.userid and user.username='" + username + "'";
    print(sql)
    ans = db.session.execute(sql)

    audiolist = ans.fetchall()  # 获取所有数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in audiolist]

    if (len(audiolist) == 0):
        data1 = {
            'status': '0',
            'message': '该用户还没有上传音频！',
            'songlists': audiolist
        }
    elif (len(audiolist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'songlists': emp_json_list
        }
    print(audiolist)
    print(emp_json_list)
    return data1

#模糊查询获取音频
@app.route('/queryaudio', methods=['post'])
def queryaudio():
    data = request.get_json(silent=True)
    username = data['username']
    query = data['query']
    sql = " select title,audiotime,isstar,type from audioinfo,user where audioinfo.userid = user.userid and user.username='" + username + "'" + " and title like '%"+query+"%'";
    print(sql)
    ans = db.session.execute(sql)

    audiolist = ans.fetchall()  # 获取所有收藏数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in audiolist]
    print(audiolist)
    if (len(audiolist) == 0):
        data1 = {
            'status': '0',
            'message': '没有该条件下的音频！',
            'songlists': audiolist,
            'url': 'http://localhost:8900/static/'
        }
    elif (len(audiolist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'songlists': emp_json_list,
            'url': ''
        }
    print(len(audiolist))
    print(emp_json_list)
    return data1

#获取收藏音频
@app.route('/getstar', methods=['post'])
def getstar():
    data = request.get_json(silent=True)
    username = data['username']
    sql = " select title,audiotime,isstar,type from audioinfo,user where audioinfo.userid = user.userid and user.username='" + username + "'" + " and audioinfo.isstar ='"+ '1' +"'";
    print(sql)
    ans = db.session.execute(sql)

    audiolist = ans.fetchall()  # 获取所有收藏数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in audiolist]
    print(audiolist)
    if (len(audiolist) == 0):
        data1 = {
            'status': '0',
            'message': '该用户还没有收藏的音频！',
            'songlists': audiolist,
            'url': 'http://localhost:8900/static/'
        }
    elif (len(audiolist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'songlists': emp_json_list,
            'url': ''
        }
    print(len(audiolist))
    print(emp_json_list)
    return data1

#获取未收藏音频
@app.route('/getnotstar', methods=['post'])
def getnotstar():
    data = request.get_json(silent=True)
    username = data['username']
    sql = " select title,audiotime,isstar,type from audioinfo,user where audioinfo.userid = user.userid and user.username='" + username + "'" + " and audioinfo.isstar ='"+ '0' +"'";
    print(sql)
    ans = db.session.execute(sql)

    audiolist = ans.fetchall()  # 获取所有收藏数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in audiolist]
    print(audiolist)
    if (len(audiolist) == 0):
        data1 = {
            'status': '0',
            'message': '该用户的音频均已被收藏！',
            'songlists': audiolist,
            'url': 'http://localhost:8900/static/'
        }
    elif (len(audiolist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'songlists': emp_json_list,
            'url': ''
        }
    print(len(audiolist))
    print(emp_json_list)
    return data1

#模糊查询获取收藏音频
@app.route('/querystaraudio', methods=['post'])
def querystaraudio():
    data = request.get_json(silent=True)
    username = data['username']
    query = data['query']
    sql = " select title,audiotime,isstar,type from audioinfo,user where audioinfo.userid = user.userid and user.username='" + username + "'" + " and audioinfo.isstar ='"+ '1' + "'" + " and title like '%"+query+"%'";
    print(sql)
    ans = db.session.execute(sql)

    audiolist = ans.fetchall()  # 获取所有收藏数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in audiolist]
    print(audiolist)
    if (len(audiolist) == 0):
        data1 = {
            'status': '0',
            'message': '没有该条件下的音频！',
            'songlists': audiolist,
            'url': 'http://localhost:8900/static/'
        }
    elif (len(audiolist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'songlists': emp_json_list,
            'url': ''
        }
    print(len(audiolist))
    print(emp_json_list)
    return data1

#模糊查询获取未收藏音频
@app.route('/querynotstaraudio', methods=['post'])
def querynotstaraudio():
    data = request.get_json(silent=True)
    username = data['username']
    query = data['query']
    sql = " select title,audiotime,isstar,type from audioinfo,user where audioinfo.userid = user.userid and user.username='" + username + "'" + " and audioinfo.isstar ='"+ '0' + "'" + " and title like '%"+query+"%'";
    print(sql)
    ans = db.session.execute(sql)

    audiolist = ans.fetchall()  # 获取所有收藏数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in audiolist]
    print(audiolist)
    if (len(audiolist) == 0):
        data1 = {
            'status': '0',
            'message': '没有该条件下的音频！',
            'songlists': audiolist,
            'url': 'http://localhost:8900/static/'
        }
    elif (len(audiolist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'songlists': emp_json_list,
            'url': ''
        }
    print(len(audiolist))
    print(emp_json_list)
    return data1

#取消收藏音频
@app.route('/canclestar', methods=['post'])
def canclestar():
    data = request.get_json(silent=True)
    username = data['username']
    title = data['title']
    try:
        sql = " update audioinfo,user set isstar ='" + '0' + "'" + "where audioinfo.userid = user.userid and user.username='" + username + "'" + "and title='" + title + "'" + "and username='" + username +"'";
        print(sql)
        db.session.execute(sql)
        db.session.commit()
        data1 = {
            'status': '1',
            'message': '取消收藏成功'
        }
    except (Exception):
        data1 = {
            'status': '0',
            'message': '取消收藏失败'
        }
    return data1

#收藏音频
@app.route('/star', methods=['post'])
def star():
    data = request.get_json(silent=True)
    username = data['username']
    title = data['title']
    try:
        sql = " update audioinfo,user set isstar ='" + '1' + "'" + "where audioinfo.userid = user.userid and user.username='" + username + "'" + "and title='" + title + "'" + "and username='" + username +"'";
        print(sql)
        db.session.execute(sql)
        db.session.commit()
        data1 = {
            'status': '1',
            'message': '收藏成功'
        }
    except (Exception):
        data1 = {
            'status': '0',
            'message': '收藏失败'
        }
    return data1

#上传音频
@app.route('/Upaudio',methods=['post'])
def upaudio():
    audiofile = request.files.get('audio')
    filename = request.form['filename']
    username = request.form['username']
    audiotime = datetime.now()
    project_file_path = os.path.dirname(
        os.path.abspath("app.py")) + os.sep + "static" + os.sep
    try:
        sql="select userid from user where username = '" +username+ "'";
        ans = db.session.execute(sql)
        getid = ans.fetchall()  # 获取所有数据
        userid = getid[0][0]
        #上传到数据库
        audio =audioinfo(userid=userid,title=filename,audiotime=audiotime,isstar='0',type='降噪前')
        db.session.add(audio)
        db.session.commit()

        # 保存到本地文件夹
        audiofile.filename = filename
        file_path = os.path.join(project_file_path, audiofile.filename)
        audiofile.save(file_path)
        # 返回值
        dictsum = {}
        dictsum['status'] = "1"
        dictsum['message'] = "上传成功"
        dictsum['url'] = "http://localhost:8900/static/" + audiofile.filename
    except Exception as e:
        print(e)
        dictsum = {}
        dictsum['status'] = "0"
        dictsum['message'] = "上传失败"
    return jsonify(dictsum)

#降噪处理
@app.route('/rnn', methods=['post'])
def rnn():
    # 获取待降噪音频 http://localhost:8900/static/demo_input_2.wav
    path = request.form['path']
    username = request.form['username']
    print(path)
    mp3 = os.path.dirname(os.path.abspath("app.py")) + os.sep + "static" + os.sep + path[29:]
    input_file=mp3
    if(path[-3:]=='mp3'):
      newpath = path[0:-4] + 'mp3new' + path[-4:]
      # 从本地获取MP3音频文件的路径
      # MP3文件转换成wav文件
      cmd = "ffmpeg -i " + mp3 + " " + mp3[0:-4] + "mp3.wav"  # 将input_path路径下所有音频文件转为.wav文件
      subprocess.call(cmd, shell=True)
      # 从本地获取转换后的wav音频文件的路径
      input_file = mp3[0:-4] + 'mp3.wav'
    elif(path[-3:]=='wav'):
        newpath = path[0:-4] + 'new' + path[-4:]
    out_file = input_file[0:-4] + 'new.raw'
    x, fs = read(input_file)
    f = wave.open(input_file)
    channels = f.getnchannels()
    sampwidth = f.getsampwidth()
    # 进行降噪处理
    main = os.path.dirname(os.path.abspath("app.py")) + os.sep +"rnnoise-master\\VisualStudio2019\\x64\\Release\\rnnoise_demo.exe"  # c++生成的exe文件执行位置
    a = os.system(main + ' ' + input_file + ' ' + out_file)  # 调用os.sysytem函数，函数以空格隔开这里参数为input_file,out_file

    if (path[-3:] == 'wav'):
      # raw转为wav
      inf_str = out_file
      outf_str = out_file[0:-4]+'.wav'
      sampleRate = fs
      pcmfile = open(inf_str, 'rb')
      pcmdata = pcmfile.read()
      wavfile = wave.open(outf_str, 'wb')
      wavfile.setframerate(sampleRate)
      wavfile.setsampwidth(sampwidth)  # 16位采样即为2字节
      wavfile.setnchannels(channels)
      wavfile.writeframes(pcmdata)
      wavfile.close()
    elif (path[-3:] == 'mp3'):
        # raw转为mp3
        inf_str = out_file
        outf_str = out_file[0:-4] + '.mp3'
        sampleRate = fs
        pcmfile = open(inf_str, 'rb')
        pcmdata = pcmfile.read()
        wavfile = wave.open(outf_str, 'wb')
        wavfile.setframerate(sampleRate)
        wavfile.setsampwidth(sampwidth)  # 16位采样即为2字节
        wavfile.setnchannels(channels)
        wavfile.writeframes(pcmdata)
        wavfile.close()

    #判断处理结果是否成功，并返回处理后的音频路径
    if (a!=0) :
        data1 = {
            'status': '0',
            'message': '降噪失败',
            'url': ''
        }
    elif(a==0):
        data1 = {
            'status': '1',
            'message': '降噪成功',
            'url': newpath
        }
        # 将降噪后音频上传到数据库
        audiotime = datetime.now()
        sql = "select userid from user where username = '" + username + "'";
        ans = db.session.execute(sql)
        getid = ans.fetchall()  # 获取所有数据
        userid = getid[0][0]
        audio = audioinfo(userid=userid, title=newpath[29:], audiotime=audiotime, isstar='0',type='降噪后')
        db.session.add(audio)
        db.session.commit()
    return data1

#删除音频
@app.route('/delete', methods=['post'])
def delete():
    # 获取用户名和音频名称
    data = request.get_json(silent=True)
    musicname = data['musicname']
    username = data['username']
    # 获取用户id
    sql = "select userid from user where username = '" + username + "'";
    ans = db.session.execute(sql)
    getid = ans.fetchall()  # 获取所有数据
    userid = getid[0][0]

    #删除该用户的该音频
    sql = "delete from audioinfo where userid = '" + str(userid) + "'" + " and title = '" + musicname + "'";
    print(sql)
    db.session.execute(sql)
    db.session.commit()
    project_file_path = os.path.dirname(os.path.abspath("app.py")) + os.sep + "static" + os.sep
    file_path = os.path.join(project_file_path, musicname)
    os.remove(file_path)
    if(musicname[-7:-4]=='new'):
        file_path1 = os.path.join(project_file_path, musicname[0:-4]+'.raw')
        os.remove(file_path1)
    # 返回值
    dictsum = {}
    dictsum['status'] = "1"
    dictsum['message'] = "删除成功"

    return jsonify(dictsum)

#获取用户信息
@app.route('/getuser', methods=['post'])
def getuser():
    data = request.get_json(silent=True)
    username = data['username']
    sql = " select * from user where user.username='" + username + "'";
    print(sql)
    ans = db.session.execute(sql)

    userlist = ans.fetchall()  # 获取所有数据
    emp_json_list = [dict(zip(item.keys(), item)) for item in userlist]

    if (len(userlist) == 0):
        data1 = {
            'status': '0',
            'message': '查询失败！',
            'userlists': ''
        }
    elif (len(userlist) > 0):
        data1 = {
            'status': '1',
            'message': '查询成功',
            'userlists': emp_json_list
        }
    print(userlist)
    print(emp_json_list)
    return data1

#修改用户信息
@app.route('/modifyuser', methods=['post'])
def modifyuser():
    data = request.get_json(silent=True)
    for i in data:
        if(data[i]==None):
            data[i] = ''
    username = data['username']
    password = data['password']
    phone = data['phone']
    gender = data['gender']
    age = data['age']
    email = data['email']
    country = data['country']

    try:
        sql = "update user set password ='" + password + "', " + "phone='" + phone + "', "  + "gender='" + gender + "', " + "age='" + age + "', " + "email='" + email + "', " + "country='" + country + "'" +" where username='" + username + "'";
        print("ceshi")
        print(sql)
        print("ceshi")
        db.session.execute(sql)
        print("ceshi")
        db.session.commit()
        print("ceshi")
        data1 = {
            'status': '1',
            'message': '用户信息修改成功'
        }
    except (Exception):
        data1 = {
            'status': '0',
            'message': '用户信息修改失败'
        }
    return data1

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8900)

