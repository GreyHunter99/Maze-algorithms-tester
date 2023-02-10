from flask import Flask, render_template, redirect, url_for
from maze import *
app = Flask(__name__)

last_maze = Maze(10)


@app.route('/')
def index():
    """ Main page """
    return redirect(url_for("visualisation"))
    # return render_template('index.html')


@app.route('/visualisation')
def visualisation():
    """ Algorithm visualisation """
    global last_maze

    return render_template('visualisation.html', maze=last_maze)


@app.route('/generate')
def generate():
    """ Generate maze """
    global last_maze

    last_maze = Maze(10)
    return redirect(url_for("visualisation"))


@app.route('/solve')
def solve():
    """ Solve maze """
    global last_maze

    last_maze.ai()
    return redirect(url_for("visualisation"))


@app.route('/clear')
def clear():
    """ Clear maze """
    global last_maze

    last_maze.clear()
    return redirect(url_for("visualisation"))


if __name__ == '__main__':
    app.run()
