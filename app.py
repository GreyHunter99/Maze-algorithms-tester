from flask import Flask, render_template, request, redirect, url_for
from test import *
app = Flask(__name__)

last_maze = Maze(10, 0, False)
test = Test(10, 10, 10, ['0'], ['0'], False)


@app.route('/')
def index():
    """ Main page """
    return render_template('index.html')


@app.route('/testing', methods=['GET', 'POST'])
def testing():
    """ Algorithm testing """
    global test
    if request.form:
        test = Test(0, 0, 0, [], [], False)
        if request.form.get('loops'):
            test.loops = True
        if request.form.get('number_of_mazes', type=int) in range(1, 51):
            test.number_of_mazes = int(request.form['number_of_mazes'])
            if request.form.get('number_of_solutions', type=int) in range(1, 51):
                test.number_of_solutions = int(request.form['number_of_solutions'])
                if request.form.get('size', type=int) in range(1, 31):
                    test.size = int(request.form['size'])
                    if request.form.get('generations', type=list) and all(x.isdigit() and int(x) in range(4) for x in request.form.getlist('generations')):
                        test.generations = request.form.getlist('generations')
                        if request.form.get('ais', type=list) and all(y.isdigit() and int(y) in range(4) for y in request.form.getlist('ais')):
                            test.ais = request.form.getlist('ais')
                            test.testing()
                            return redirect(url_for("testing"))
    names = {"generations": {0: "recursive backtracker", 1: "algorytm Kruskala", 2: "algorytm Prima"}, "ais": {0: "losowa mysz", 1: "wall follower", 2: "algorytm Pledge'a"}}
    return render_template('testing.html', test=test, names=names)


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
    generation = 0
    loops = False
    if request.form.get('size', type=int) in range(31):
        size = int(request.form['size'])
    if request.form.get('generation', type=int) in range(4):
        generation = int(request.form['generation'])
    if 'loops' in request.form:
        loops = True
    last_maze = Maze(size, generation, loops)
    return redirect(url_for("visualisation"))


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    """ Solve maze """
    global last_maze
    if request.form.get('ai') == "0":
        last_maze.random_mouse()
    if request.form.get('ai') == "1":
        last_maze.wall_follower()
    if request.form.get('ai') == "2":
        last_maze.pledge()
    return redirect(url_for("visualisation"))


@app.route('/clear')
def clear():
    """ Clear maze """
    global last_maze
    last_maze.clear()
    return redirect(url_for("visualisation"))


if __name__ == '__main__':
    app.run()
