from flask import Flask, render_template
import os
app = Flask(__name__)


@app.route('/music')
def music():
    path = os.path.dirname(os.path.abspath(__file__))
    path = path + '/static/music/'
    all_files = os.listdir(path)
    music_list = []
    for i in all_files:
        print(i)
        music_list.append(i)
    # music_list = Markup(music_list) Markup返回的是字符串，这会导致页面中{{ music_list[0] }}异常，所以应该在页面中用safe或tojson标记
    return render_template('music.html', music_list=music_list)


if __name__ == '__main__':
    app.run()