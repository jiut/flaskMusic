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
    music_list = [{"name": "请发起搜索", "link": "/"}]
    return render_template("music_test.html", music_list=music_list, title="测试")


@app.route('/musictest', methods=["GET"])
def musicSearch():
    f_search = open('./SearchCache.txt', 'r+', encoding="utf-8")
    search_cache = eval(f_search.readline())
    f_value = open('./ValueCache.txt', 'r+', encoding="utf-8")
    value_cache = eval(f_value.readline())

    is_value_change = 0

    key = request.args.get('key')

    if key in search_cache:
        search = search_cache[key]
    else:
        search = requests.get(url + "/cloudsearch?keywords=" + key).json()
        search_cache[key] = search
        f_search.truncate(0)
        f_search.write(str(search_cache).strip())

    f_search.close()

    songs = search['result']['songs']
    music_list = {"result": []}
    for song in songs:
        name = song["name"]
        id = song["id"]
        # if (id in value_cache) and ("link" in value_cache[id]) and (requests.get(value_cache[id]["link"]).status_code == 200):
        #     link = value_cache[id]["link"]
        # else:
        #     link = requests.get(url + "/song/url?id=" + str(id)).json()
        #     link = link['data'][0]['url']
        #
        #     value_cache[id].update({"link": link})
        #     is_value_change = is_value_change + 1

        if (id in value_cache) and ("lrc" in value_cache[id]):
            lrc = value_cache[id]["lrc"]
        else:
            lrc = requests.get(url + "/lyric?id=" + str(id)).json()
            lrc = lrc["lrc"]["lyric"]
            if( id in value_cache):
                value_cache[id].update({"lrc": lrc})
            else:
                value_cache[id] = {"lrc": lrc}
            is_value_change = is_value_change + 1

        is_value_change = False

        ar = song["ar"]
        al = song["al"]

        artist_list = ''
        for artist in ar:
            artist_list = artist_list + artist['name'] + '/'

        artist_list = artist_list[:-1]
        dict = {"id": id, "name": name, "ar": artist_list, "lrc": lrc, "alPic": al['picUrl'] + "?param=130y130"}
        # dict = {"id": id, "name": name, "ar": ar, "lrc": lrc, "alPic": al}

        music_list["result"].append(dict)

    if is_value_change > 0:
        f_value.truncate(0)
        f_value.write(str(value_cache).strip())
    f_value.close()
    return music_list

@app.route("/query-url")
def QueryUrl():
    key = request.args.get('id')
    f_link = open('./LinkCache.txt', 'r+', encoding="utf-8")
    link_cache = eval(f_link.readline())

    if id in link_cache:
        link = link_cache[id]["link"]
    else:
        link = requests.get(url + "/song/url?id=" + str(id)).json()
        link = link['data'][0]['url']
        req = requests.get(link)
        link = url_for('static', filename='/music/'+ str(id) + ".mp3")
        with open(link, "wb") as f:
            f.write(req.content)

    return link


if __name__ == '__main__':
    app.run()
