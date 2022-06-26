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
    return render_template('music.html', music_list=music_list)


if __name__ == '__main__':
    app.run()