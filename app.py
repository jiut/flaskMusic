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

            text = requests.get(url + "/login/cellphone?phone=" + username + "&captcha=" + password).status_code
            flash('input.' + str(text))
            return redirect(url_for('login'))

    return render_template("login.html", title="登录")


@app.route('/login/<int:phone>')
def phoneLogin(phone):
    requests.get(url + "/captcha/sent?phone=" + str(phone))
    return None

@app.route('/loginstatus')
def loginstatus():
    code = requests.get(url + "/login/status")
    return str(code)

@app.route('/test', methods=['GET'])
def test():
    music_list = [{"name": "请发起搜索", "link": "/"}]
    return render_template("music_test.html", music_list=music_list, title="测试")


@app.route('/musictest/', methods=["GET"])
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
        f_search.seek(0)  # 得把指针移动到开头再truncate才行，要不然会出现NUL
        f_search.truncate(0)
        write_line = str(search_cache)
        f_search.write(write_line)

    f_search.close()

    songs = search['result']['songs']
    music_list = {"result": []}
    for song in songs:
        name = song["name"]
        id = song["id"]

        if (id in value_cache) and ("lrc" in value_cache[id]):
            lrc = value_cache[id]["lrc"]
        else:
            lrc = requests.get(url + "/lyric?id=" + str(id)).json()
            lrc = lrc["lrc"]["lyric"]
            if (id in value_cache):
                value_cache[id].update({"lrc": lrc})
            else:
                value_cache[id] = {"lrc": lrc}
            is_value_change = is_value_change + 1

        ar = song["ar"]
        al = song["al"]

        artist_list = ''
        for artist in ar:
            artist_list = artist_list + artist['name'] + '/'

        artist_list = artist_list[:-1]
        dict = {"id": id, "name": name, "ar": artist_list, "alPic": al['picUrl'] + "?param=130y130", "lrc": lrc}
        # dict = {"lrc": lrc, "alPic": al,  "ar": ar, "name": name, "id": id}

        music_list["result"].append(dict)

    if is_value_change > 0:
        f_value.seek(0)
        f_value.truncate(0)
        write_line = str(value_cache)
        f_value.write(write_line)
    f_value.close()
    return music_list


@app.route("/queryurl/<id>")#链接
def queryurl(id):
    f_link = open('./LinkCache.txt', 'r+', encoding="utf-8")
    link_cache = eval(f_link.readline())

    if id in link_cache:
        link = url_for("static", filename="music/" + id + '.mp3')
    else:
        link = requests.get(url + "/song/url?id=" + id).json()
        if "data" in link:
            link = link['data'][0]['url']
        else:
            return "/"

        temp_link = url_for('static', filename='music/' + id + ".mp3")
        req = requests.get(link)
        with open("." + temp_link, "wb") as f:
            f.write(req.content)

        link = temp_link

        link_cache.add(id)
        f_link.seek(0)
        f_link.truncate(0)
        f_link.write(str(link_cache))

    f_link.close()

    return redirect(link)


# @app.route("/querylrc/<id>")#歌词
# def querylrc(id):
#     f_value = open('./ValueCache.txt', 'r+', encoding="utf-8")
#     value_cache = eval(f_value.readline())
#
#     if (id in value_cache) and ("lrc" in value_cache[id]):
#         lrc = value_cache[id]["lrc"]
#     else:
#         lrc = requests.get(url + "/lyric?id=" + id).json()
#         lrc = lrc["lrc"]["lyric"]
#         value_cache[id] = {"lrc": lrc}
#
#         f_value.seek(0)
#         f_value.truncate(0)
#         write_line = str(value_cache)
#         f_value.write(write_line)
#
#     f_value.close()
#
#     return lrc


# def downloader(id, link):
#     id = request.args.get("id")
#     temp_link = url_for('static', filename='music/' + id + ".mp3")
#
#     link = request.args.get("link")
#     req = requests.get(link)
#     with open("." + temp_link, "wb") as f:
#         f.write(req.content)
#     return "complete"
#
#
# @app.route("/downloadtest")
# def downloadtest():
#     redirect(url_for("downloader",
#                      link="http://m8.music.126.net/20220701173048/9d7187d4010629789a4d93835605134f/ymusic/obj/w5zDlMODwrDDiGjCn8Ky/14054238118/3937/706d/7e7b/a65b577e39ee0d8c88a2936b409f7300.mp3",
#                      id="1913532415"))
#
#     return "test"


if __name__ == '__main__':
    app.run()
