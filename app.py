# 需要网易云api


import requests
from flask import Flask, render_template, url_for, redirect, flash, request

app = Flask(__name__)
app.secret_key = 'dev'

url = "http://localhost:3000"

@app.route('/')
def music():
    music_list = [{"name": "请发起搜索", "link": "/"}]
    return render_template("music_test.html", music_list=music_list, title="首页")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'submit' in request.form:
            username = request.form['username']
            password = request.form['password']

            text = requests.get(url + "/login/cellphone?phone=" + username + "&captcha=" + password).text
            flash('input.' + text)
            return redirect(url_for('login'))


    return render_template("login.html", title="登录")

@app.route('/login/<int:phone>')
def phoneLogin(phone):
    requests.get(url + "/captcha/sent?phone=" + str(phone))
    return None

@app.route('/test', methods=['GET'])
def test():
    music_list = [{"name":"请发起搜索", "link":"/"}]
    return render_template("music_test.html", music_list=music_list, title="测试")


@app.route('/musictest', methods=["GET"])
def musicSearch():
    f1 = open('./test1.txt', 'a', encoding="utf-8")
    f1.truncate(0)
    f2 = open('./test2.txt', 'a', encoding="utf-8")
    f2.truncate(0)

    key = request.args.get('key')
    search = requests.get(url + "/cloudsearch?keywords=" + key).json()
    f1.write(str(search))
    f1.close()

    text = search['result']['songs']
    music_list = {"result":[]}
    target = {"result":[]}
    for song in text:
        name = song["name"]
        id = song["id"]
        origin = requests.get(url + "/song/url?id=" + str(id)).json()
        link = origin['data'][0]['url']
        dict = {"name": name, "link": link}

        ar = song["ar"]
        al = song["al"]
        alia = []
        if(song["alia"]):
            alia = song["alia"]
        dict2 = {"name":name, "id":id, "ar":ar, "al":al, "alia":alia}
        # print(dict)
        target["result"].append(dict2)

        music_list["result"].append(dict)
    flash(str(target))
    f2.write(str(target))
    f2.close()
    return music_list

if __name__ == '__main__':
    app.run()
