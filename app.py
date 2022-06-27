# 需要网易云api


import requests
from flask import Flask, render_template, url_for, redirect, flash, request

app = Flask(__name__)
app.secret_key = 'dev'

url = "http://localhost:3000"


@app.route('/')
def music():
    music_list = [{
        "link": "http://m702.music.126.net/20220627163639/1bce7261f9c9f19e31efd87cac238a92/jd-musicrep-ts/4600/a5fa/c85f/555d31856cd048d0635a8903e3fdce2c.mp3",
        "name": "海阔天空"}, {
        "link": "http://m7.music.126.net/20220627163640/5368973424a8802f561489af210b8704/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/3293982182/6b94/780d/f60c/863291955df7f34ba1bd09f45fbc38d4.mp3",
        "name": "海阔天空 (Live)"}]

    if request.method == 'POST':
        target = request.form["search"]
        search = requests.get(url + "/cloudsearch?keywords=" + target).json()

        text = search['result']['songs']
        music_list = []
        for song in text:
            name = song["name"]
            id = song["id"]
            origin = requests.get(url + "/song/url?id=" + str(id)).json()
            link = origin['data'][0]['url']
            dict = {"name": name, "link": link}
            print(dict)
            music_list.append(dict)
    return render_template("music_test.html", music_list=music_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'submit' in request.form:
            username = request.form['username']
            password = request.form['password']

            # if not username or not password:
            #     flash('Invalid input.')
            #     return redirect(url_for('login'))
            #
            # user = User.query.first()
            #
            # if username == user.username and user.validate_password(password):
            #     login_user(user)
            #     flash('Login success.')
            #     return redirect(url_for('index'))
            #
            # flash('Invalid username or password.')
            # return redirect(url_for('login'))
            text = requests.get(url + "/login/cellphone?phone=" + username + "&captcha=" + password).text
            # text = url + "/login/cellphone?phone=" + username + "&captcha=" + password
            flash('input.' + text)
            return redirect(url_for('login'))
            print(username)
            print(password)

        if 'validate' in request.form:
            username = request.form['username']
            requests.get(url + "/captcha/sent?phone=" + username)

    return render_template("login.html")


@app.route('/test', methods=['GET', 'POST'])
def test():
    music_list = [{
                      "link": "http://m702.music.126.net/20220627163639/1bce7261f9c9f19e31efd87cac238a92/jd-musicrep-ts/4600/a5fa/c85f/555d31856cd048d0635a8903e3fdce2c.mp3",
                      "name": "海阔天空"}, {
                      "link": "http://m7.music.126.net/20220627163640/5368973424a8802f561489af210b8704/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/3293982182/6b94/780d/f60c/863291955df7f34ba1bd09f45fbc38d4.mp3",
                      "name": "海阔天空 (Live)"}]

    if request.method == 'POST':
        target = request.form["search"]
        search = requests.get(url + "/cloudsearch?keywords=" + target).json()

        text = search['result']['songs']
        music_list = []
        for song in text:
            name = song["name"]
            id = song["id"]
            origin = requests.get(url + "/song/url?id=" + str(id)).json()
            link = origin['data'][0]['url']
            dict = {"name": name, "link": link}
            print(dict)
            music_list.append(dict)
    return render_template("music_test.html", music_list=music_list)


if __name__ == '__main__':
    app.run()
