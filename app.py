from flask import Flask, render_template
from maze import *
app = Flask(__name__)


@app.route('/')
def index():
    """ Main page """
    maze = Maze(10)
    return render_template('index.html', maze=maze)


if __name__ == '__main__':
    app.run()
