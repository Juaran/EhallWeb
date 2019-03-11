from flask import Flask, render_template, url_for, redirect, request, flash, session
from config import MainConfig
from preLogin import loginResult
from showData import show
import os


app = Flask(__name__)
app.config.from_object(MainConfig)
app.secret_key = os.urandom(24)


@app.route('/')
def prelogin():
    return redirect(url_for("login"))  # 重定向到登录


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # get 登录界面

        flash("首次登录请耐心等待...")
        return render_template("login.html")

    if request.method == "POST":  # 在登录界面提交表单

        username = request.form.get("username")  # 获取username
        password = request.form.get("password")  # 获取password

        """ 登录校验 """
        if username != '' and password != '' and username.isdigit() and len(username)==11:

            login_result = loginResult.get_result(username, password)

            if login_result:
                # 登录成功
                flash("登录成功！")
                return redirect(url_for("index", username=username))  # 登录成功跳转首页

            else:
                # 登录失败
                flash("登录失败！")  # 页面显示闪现消息
                return render_template("login.html")
        else:
            flash("登录失败！")  # 页面显示闪现消息
            return render_template("login.html")


username, term = '', ''


@app.route('/index/')
def index():

    global username, term
    username = request.args.get("username")
    term = str(int(username[:4]) - 1) + "-" + username[:4] + "-2"

    return render_template("index.html", username=username)


@app.route('/welcome/')
def welcome():
    username = request.args.get("username")
    return render_template("welcome.html", username=username)


@app.route('/index/<username>/course/', methods=['POST', 'GET'])
def course(username):

    global term

    if request.method == 'GET':
        courses = show.Show(username).course(term)

        if courses is not None:
            return render_template("course.html", courses=courses, term=int(username[:4]), username=username)
        else:
            term = "2017-2018-1"
            return render_template("nothing.html")
#
# @app.route('/term/', methods=['POST'])
# def term():
    if request.method == 'POST':
        chooseTerm = request.get_data().decode("utf-8")

        year = chooseTerm[:4]
        season = "1"
        if chooseTerm[5] == "秋":
            season = "2"

        term = str(int(year)-1) + "-" + year + "-" + season
        print(term)
        return "选取学期", term


@app.route('/index/<username>/grades/', methods=['POST', 'GET'])
def grades(username):

    global term

    if request.method == "GET":
        grades = show.Show(username).grades(term)
        if grades is not None:
            return render_template("grades.html", grades=grades, term=int(username[:4]), username=username)
        else:
            term = "2017-2018-1"
            return render_template("nothing.html")

    if request.method == 'POST':
        chooseTerm = request.get_data().decode("utf-8")

        year = chooseTerm[:4]
        season = "1"
        if chooseTerm[5] == "秋":
            season = "2"

        term = str(int(year) - 1) + "-" + year + "-" + season
        print(term)
        return "选取学期", term


@app.route('/index/<username>/exams/', methods=['POST', 'GET'])
def exams(username):
    global term

    if request.method == "GET":
        exams = show.Show(username).exam(term)
        if exams is not None:
            return render_template("exams.html", exams=exams, term=int(username[:4]), username=username)
        else:
            term = "2017-2018-1"
            return render_template("nothing.html")

    if request.method == 'POST':
        chooseTerm = request.get_data().decode("utf-8")

        year = chooseTerm[:4]
        season = "1"
        if chooseTerm[5] == "秋":
            season = "2"

        term = str(int(year) - 1) + "-" + year + "-" + season
        print(term)
        return "选取学期", term


if __name__ == '__main__':
    app.run(port=8080)
