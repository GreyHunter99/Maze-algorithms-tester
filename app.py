from flask import Flask, render_template, request, redirect, url_for
from maze import *
app = Flask(__name__)

last_maze = Maze(10, 0, False)


@app.route('/')
def index():
    """ Main page """

    return render_template('index.html')


@app.route('/visualisation')
def visualisation():
    """ Algorithm visualisation """
    global last_maze

    return render_template('visualisation.html', maze=last_maze)


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """ Generate maze """
    global last_maze
    size = 10
    algorithm = 0
    loops = False

    if request.form.get('size') == "5":
        size = 5
    elif request.form.get('size') == "10":
        size = 10

    if request.form.get('algorithm') == "0":
        algorithm = 0
    elif request.form.get('algorithm') == "1":
        algorithm = 1

    if 'loops' in request.form:
        loops = True

    last_maze = Maze(size, algorithm, loops)
    return redirect(url_for("visualisation"))


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    """ Solve maze """
    global last_maze

    if 'ai' in request.form and request.form['ai'] == "0":
        last_maze.random_mouse()

    return redirect(url_for("visualisation"))


@app.route('/clear')
def clear():
    """ Clear maze """
    global last_maze

    last_maze.clear()
    return redirect(url_for("visualisation"))


if __name__ == '__main__':
    app.run()
