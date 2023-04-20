from flask import Flask, render_template, request, redirect, url_for, session
from test import *

app = Flask(__name__)
app.secret_key = "super secret key"

ids = 1
mazes = {}
tests = {}
names = {"generations": {0: "recursive backtracker", 1: "algorytm Kruskala", 2: "algorytm Prima", 3: "algorytm Wilsona"}, "ais": {0: "losowa mysz", 1: "wall follower", 2: "algorytm Pledge'a", 3: "algorytm Trémauxa"}}


@app.route('/')
def index():
    """ Main page """
    return render_template('index.html')


@app.route('/testing', methods=['GET', 'POST'])
def testing():
    """ Algorithm testing """
    global ids, tests, names
    if not session.get('id'):
        session['id'] = ids
        ids += 1
    if not session['id'] in tests or request.form:
        tests[session['id']] = Test(10, 10, 10, ['0'], ['0'])
    test = tests[session['id']]
    if request.form.get('number_of_mazes', type=int) in range(1, 101):
        test.number_of_mazes = int(request.form['number_of_mazes'])
        if request.form.get('number_of_solutions', type=int) in range(1, 51):
            test.number_of_solutions = int(request.form['number_of_solutions'])
            if request.form.get('size', type=int) in range(1, 31):
                test.size = int(request.form['size'])
                if request.form.get('generations', type=list) and all(x.isdigit() and int(x) in range(4) for x in request.form.getlist('generations')):
                    test.generations = request.form.getlist('generations')
                    if request.form.get('ais', type=list) and all(y.isdigit() and int(y) in range(4) for y in request.form.getlist('ais')):
                        test.ais = request.form.getlist('ais')
                        if request.form.get('loops'):
                            test.loops = True
                        test.testing()
    if request.form:
        return redirect(url_for("testing"))
    return render_template('testing.html', test=test, names=names)


@app.route('/visualisation')
def visualisation():
    """ Algorithm visualisation """
    global mazes, names
    if session.get('id') and session['id'] in mazes:
        maze = mazes[session['id']]
    else:
        maze = None
    return render_template('visualisation.html', maze=maze, names=names)


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """ Generate maze """
    global ids, mazes
    if not session.get('id'):
        session['id'] = ids
        ids += 1
    if request.form.get('size', type=int) in range(31):
        size = int(request.form['size'])
        if request.form.get('generation', type=int) in range(4):
            generation = int(request.form['generation'])
            loops = False
            if 'loops' in request.form:
                loops = True
            mazes[session['id']] = Maze(size, generation, loops)
    return redirect(url_for("visualisation"))


@app.route('/solve', methods=['GET', 'POST'])
def solve():
    """ Solve maze """
    global mazes
    if session.get('id') and session['id'] in mazes:
        if request.form.get('ai') == "0":
            mazes[session['id']].random_mouse()
        if request.form.get('ai') == "1":
            mazes[session['id']].wall_follower()
        if request.form.get('ai') == "2":
            mazes[session['id']].pledge()
        if request.form.get('ai') == "3":
            mazes[session['id']].tremaux()
    return redirect(url_for("visualisation"))


@app.route('/clear')
def clear():
    """ Clear maze """
    global mazes
    if session.get('id') and session['id'] in mazes:
        mazes[session['id']].clear()
    return redirect(url_for("visualisation"))


if __name__ == '__main__':
    app.run()
