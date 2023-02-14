import random
from cell import *


class Maze:
    """ Maze class """
    def __init__(self, size, algorithm, loops):
        self.size = size
        self.algorithm = algorithm
        self.loops = loops
        self.ai = ''
        self.end = self.choose_end()
        self.spawn = self.choose_spawn()
        self.moves = 0
        if self.algorithm == 0:
            self.cells = self.recursive_backtracker()
        elif self.algorithm == 1:
            self.cells = self.kruskal()
        if self.loops:
            self.remove_random_walls()
        self.clear()

    def recursive_backtracker(self):
        cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        current_cell = cells[self.end[0]][self.end[1]]
        current_cell.visited = True
        stack = [current_cell]
        while True:
            neighbours = dict()
            if current_cell.x > 0 and not cells[current_cell.x - 1][current_cell.y].visited:
                neighbours['left'] = cells[current_cell.x - 1][current_cell.y]
            if current_cell.x < self.size - 1 and not cells[current_cell.x + 1][current_cell.y].visited:
                neighbours['right'] = cells[current_cell.x + 1][current_cell.y]
            if current_cell.y > 0 and not cells[current_cell.x][current_cell.y - 1].visited:
                neighbours['bottom'] = cells[current_cell.x][current_cell.y - 1]
            if current_cell.y < self.size - 1 and not cells[current_cell.x][current_cell.y + 1].visited:
                neighbours['top'] = cells[current_cell.x][current_cell.y + 1]
            if len(neighbours) > 0:
                chosen_neighbour = random.choice(list(neighbours.items()))
                next_cell = chosen_neighbour[1]
                if chosen_neighbour[0] == 'top':
                    current_cell.walls['top'] = False
                    next_cell.walls['bottom'] = False
                if chosen_neighbour[0] == 'bottom':
                    current_cell.walls['bottom'] = False
                    next_cell.walls['top'] = False
                if chosen_neighbour[0] == 'left':
                    current_cell.walls['left'] = False
                    next_cell.walls['right'] = False
                if chosen_neighbour[0] == 'right':
                    current_cell.walls['right'] = False
                    next_cell.walls['left'] = False
                current_cell = next_cell
                stack.append(current_cell)
                current_cell.visited = True
            else:
                stack.pop()
                if len(stack) > 0:
                    current_cell = stack[-1]
                else:
                    break
        return cells

    def kruskal(self):
        cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        walls = []
        groups_of_cells = []
        for x in range(self.size):
            for y in range(self.size):
                groups_of_cells.append({(x, y)})
                if x < self.size - 1:
                    walls.append([(x, y), (x + 1, y), 'hor'])
                if y < self.size - 1:
                    walls.append([(x, y), (x, y + 1), 'ver'])
        while walls:
            wall = random.choice(walls)
            id1 = 'a'
            id2 = 'b'
            for index, group in enumerate(groups_of_cells):
                if wall[0] in group:
                    id1 = index
                if wall[1] in group:
                    id2 = index
                if type(id1) == int and type(id2) == int:
                    break
            if id1 != id2:
                groups_of_cells[id1].update(groups_of_cells[id2])
                del groups_of_cells[id2]
                if wall[2] == 'ver':
                    cells[wall[0][0]][wall[0][1]].walls['top'] = False
                    cells[wall[1][0]][wall[1][1]].walls['bottom'] = False
                else:
                    cells[wall[0][0]][wall[0][1]].walls['right'] = False
                    cells[wall[1][0]][wall[1][1]].walls['left'] = False
            walls.remove(wall)
        return cells

    def random_mouse(self):
        self.ai = 0
        self.clear()
        position = self.cells[self.spawn[0]][self.spawn[1]]
        position.visited += 1
        self.moves = 0
        while position != self.cells[self.end[0]][self.end[1]]:
            neighbours = []
            if not position.walls['top']:
                neighbours.append(self.cells[position.x][position.y + 1])
            if not position.walls['bottom']:
                neighbours.append(self.cells[position.x][position.y - 1])
            if not position.walls['left']:
                neighbours.append(self.cells[position.x - 1][position.y])
            if not position.walls['right']:
                neighbours.append(self.cells[position.x + 1][position.y])
            position = random.choice(neighbours)
            position.visited += 1
            self.moves += 1

    def wall_follower(self):
        self.ai = 1
        self.clear()
        position = self.cells[self.spawn[0]][self.spawn[1]]
        position.visited += 1
        self.moves = 0
        cell_stack = [(position.x, position.y)]
        mode_list = [(0, 1), (2, -1), 0]
        mode = 0
        wall_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        wall = []
        if position.walls['top']:
            wall.append(0)
        if position.walls['right']:
            wall.append(1)
        if position.walls['bottom']:
            wall.append(2)
        if position.walls['left']:
            wall.append(3)
        if not wall:
            wall = [0, 1, 2, 3]
            mode = 2
        wall = random.choice(wall)
        while position != self.cells[self.end[0]][self.end[1]] and self.moves < 500:
            if mode == 2:
                if not position.walls[wall_order[(wall + 1) % 4][0]]:
                    position = self.cells[position.x + wall_order[wall][2]][position.y - wall_order[wall][1]]
                else:
                    wall = []
                    if position.walls['top']:
                        wall.append(0)
                    if position.walls['right']:
                        wall.append(1)
                    if position.walls['bottom']:
                        wall.append(2)
                    if position.walls['left']:
                        wall.append(3)
                    wall = random.choice(wall)
                    mode = 0
                    cell_stack = []
            if mode != 2:
                if not position.walls[wall_order[wall][0]]:
                    position = self.cells[position.x + wall_order[wall][1]][position.y + wall_order[wall][2]]
                    wall = (wall + 1 + mode_list[mode][0]) % 4
                elif not position.walls[wall_order[(wall + 3 + mode_list[mode][0]) % 4][0]]:
                    position = self.cells[position.x - mode_list[mode][1] * wall_order[wall][2]][position.y + mode_list[mode][1] * wall_order[wall][1]]
                elif position.walls[wall_order[(wall + 2) % 4][0]]:
                    position = self.cells[position.x + mode_list[mode][1] * wall_order[wall][2]][position.y - mode_list[mode][1] * wall_order[wall][1]]
                    wall = (wall + 2) % 4
                else:
                    position = self.cells[position.x - wall_order[wall][1]][position.y - wall_order[wall][2]]
                    wall = (wall + 3 + mode_list[mode][0]) % 4
                if cell_stack.count((position.x, position.y)) > 3:
                    mode = (mode + 1) % 3
                    cell_stack = []
                    wall = []
                    if position.walls['top']:
                        wall.append(0)
                    if position.walls['right']:
                        wall.append(1)
                    if position.walls['bottom']:
                        wall.append(2)
                    if position.walls['left']:
                        wall.append(3)
                    if not wall:
                        wall = [0, 1, 2, 3]
                        mode = 2
                    wall = random.choice(wall)
            cell_stack.append((position.x, position.y))
            position.visited += 1
            self.moves += 1

    def choose_spawn(self):
        spawn_points = []
        for x in range(int(self.size / 2 - self.size / 10), int(self.size / 2 + self.size / 10)):
            for y in range(int(self.size / 2 - self.size / 10), int(self.size / 2 + self.size / 10)):
                spawn_points.append((x, y))
        return random.choice(spawn_points)

    def choose_end(self):
        edges = set()
        for x in range(self.size):
            for y in range(self.size):
                if x == 0 or x == self.size - 1 or y == 0 or y == self.size - 1:
                    edges.add((x, y))
        edges = list(edges)
        return random.choice(edges)

    def remove_random_walls(self):
        i = 0
        while i < self.size ** 2 / 10:
            cell = random.choice(random.choice(self.cells))
            walls = []
            if cell.walls['top'] and cell.y != self.size - 1:
                walls.append(['top', cell.x, cell.y + 1, 'bottom'])
            if cell.walls['bottom'] and cell.y != 0:
                walls.append(['bottom', cell.x, cell.y - 1, 'top'])
            if cell.walls['left'] and cell.x != 0:
                walls.append(['left', cell.x - 1, cell.y, 'right'])
            if cell.walls['right'] and cell.x != self.size - 1:
                walls.append(['right', cell.x + 1, cell.y, 'left'])
            if walls:
                wall = random.choice(walls)
                cell.walls[wall[0]] = False
                self.cells[wall[1]][wall[2]].walls[wall[3]] = False
                i += 1

    def clear(self):
        self.moves = 0
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].visited = 0
