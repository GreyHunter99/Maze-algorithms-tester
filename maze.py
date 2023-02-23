import random
from cell import *


class Maze:
    """ Maze class """
    def __init__(self, size, generation, loops):
        self.size = size
        self.generation = generation
        self.loops = loops
        self.ai = ''
        self.end = self.choose_end()
        self.spawn = self.choose_spawn()
        self.moves = 0
        self.cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        if self.generation == 0:
            self.recursive_backtracker()
        elif self.generation == 1:
            self.kruskal()
        elif self.generation == 2:
            self.prim()
        if self.loops:
            self.remove_random_walls()
        self.clear()

    def recursive_backtracker(self):
        current_cell = self.cells[self.end[0]][self.end[1]]
        current_cell.visited = True
        stack = [current_cell]
        while True:
            neighbours = dict()
            if current_cell.x > 0 and not self.cells[current_cell.x - 1][current_cell.y].visited:
                neighbours['left'] = self.cells[current_cell.x - 1][current_cell.y]
            if current_cell.x < self.size - 1 and not self.cells[current_cell.x + 1][current_cell.y].visited:
                neighbours['right'] = self.cells[current_cell.x + 1][current_cell.y]
            if current_cell.y > 0 and not self.cells[current_cell.x][current_cell.y - 1].visited:
                neighbours['bottom'] = self.cells[current_cell.x][current_cell.y - 1]
            if current_cell.y < self.size - 1 and not self.cells[current_cell.x][current_cell.y + 1].visited:
                neighbours['top'] = self.cells[current_cell.x][current_cell.y + 1]
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

    def kruskal(self):
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
                    self.cells[wall[0][0]][wall[0][1]].walls['top'] = False
                    self.cells[wall[1][0]][wall[1][1]].walls['bottom'] = False
                else:
                    self.cells[wall[0][0]][wall[0][1]].walls['right'] = False
                    self.cells[wall[1][0]][wall[1][1]].walls['left'] = False
            walls.remove(wall)

    def prim(self):
        cell = self.cells[self.spawn[0]][self.spawn[1]]
        cell.visited = True
        walls = []
        if cell.y < self.size - 1:
            walls.append([(cell.x, cell.y), (cell.x, cell.y + 1), 'ver'])
        if cell.x < self.size - 1:
            walls.append([(cell.x, cell.y), (cell.x + 1, cell.y), 'hor'])
        if cell.y > 0:
            walls.append([(cell.x, cell.y - 1), (cell.x, cell.y), 'ver'])
        if cell.x > 0:
            walls.append([(cell.x - 1, cell.y), (cell.x, cell.y), 'hor'])
        while walls:
            wall = random.choice(walls)
            cell = False
            if not self.cells[wall[0][0]][wall[0][1]].visited:
                cell = self.cells[wall[0][0]][wall[0][1]]
            if not self.cells[wall[1][0]][wall[1][1]].visited:
                cell = self.cells[wall[1][0]][wall[1][1]]
            if cell:
                cell.visited = True
                if wall[2] == 'hor':
                    self.cells[wall[0][0]][wall[0][1]].walls['right'] = False
                    self.cells[wall[1][0]][wall[1][1]].walls['left'] = False
                else:
                    self.cells[wall[0][0]][wall[0][1]].walls['top'] = False
                    self.cells[wall[1][0]][wall[1][1]].walls['bottom'] = False
                if cell.y < self.size - 1 and not self.cells[cell.x][cell.y + 1].visited:
                    walls.append([(cell.x, cell.y), (cell.x, cell.y + 1), 'ver'])
                if cell.x < self.size - 1 and not self.cells[cell.x + 1][cell.y].visited:
                    walls.append([(cell.x, cell.y), (cell.x + 1, cell.y), 'hor'])
                if cell.y > 0 and not self.cells[cell.x][cell.y - 1].visited:
                    walls.append([(cell.x, cell.y - 1), (cell.x, cell.y), 'ver'])
                if cell.x > 0 and not self.cells[cell.x - 1][cell.y].visited:
                    walls.append([(cell.x - 1, cell.y), (cell.x, cell.y), 'hor'])
            walls.remove(wall)

    def random_mouse(self):
        self.ai = 0
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 30 * self.size ** 2:
                visited_neighbours = []
                not_visited_neighbours = []
                if not position.walls['top']:
                    if self.cells[position.x][position.y + 1].visited:
                        visited_neighbours.append(self.cells[position.x][position.y + 1])
                    else:
                        not_visited_neighbours.append(self.cells[position.x][position.y + 1])
                if not position.walls['bottom']:
                    if self.cells[position.x][position.y - 1].visited:
                        visited_neighbours.append(self.cells[position.x][position.y - 1])
                    else:
                        not_visited_neighbours.append(self.cells[position.x][position.y - 1])
                if not position.walls['left']:
                    if self.cells[position.x - 1][position.y].visited:
                        visited_neighbours.append(self.cells[position.x - 1][position.y])
                    else:
                        not_visited_neighbours.append(self.cells[position.x - 1][position.y])
                if not position.walls['right']:
                    if self.cells[position.x + 1][position.y].visited:
                        visited_neighbours.append(self.cells[position.x + 1][position.y])
                    else:
                        not_visited_neighbours.append(self.cells[position.x + 1][position.y])
                if not_visited_neighbours:
                    position = random.choice(not_visited_neighbours)
                else:
                    position = random.choice(visited_neighbours)
                position.visited += 1
                self.moves += 1
            if self.moves < 30 * self.size ** 2:
                break

    def wall_follower(self):
        self.ai = 1
        mode_list = [0, 2, '']
        direction_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            mode = 0
            cell_stack = [(position.x, position.y)]
            direction = random.randint(0, 3)
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 30 * self.size ** 2:
                if self.moves > 2 * self.size ** 2 and self.moves % (self.size ** 2 // 2) == 0 or self.moves > 3 * self.size ** 2 and self.moves % (self.size ** 2 // 3) == 0:
                    mode = (mode + 1) % 3
                    cell_stack = [(position.x, position.y)]
                    direction = random.randint(0, 3)
                if mode == 2:
                    if position.walls[direction_order[direction][0]]:
                        mode = 0
                        cell_stack = [(position.x, position.y)]
                        direction = random.randint(0, 3)
                        continue
                else:
                    if not position.walls[direction_order[(direction + 1 + mode_list[mode]) % 4][0]]:
                        direction = (direction + 1 + mode_list[mode]) % 4
                    elif not position.walls[direction_order[direction][0]]:
                        pass
                    elif not position.walls[direction_order[(direction + 3 + mode_list[mode]) % 4][0]]:
                        direction = (direction + 3 + mode_list[mode]) % 4
                    else:
                        direction = (direction + 2) % 4
                next_x = position.x + direction_order[direction][1]
                next_y = position.y + direction_order[direction][2]
                if mode != 2 and cell_stack.count((next_x, next_y)) > 3:
                    mode = (mode + 1) % 3
                    cell_stack = [(position.x, position.y)]
                    direction = random.randint(0, 3)
                    continue
                position = self.cells[next_x][next_y]
                position.visited += 1
                cell_stack.append((position.x, position.y))
                self.moves += 1
            if self.moves < 30 * self.size ** 2:
                break

    def pledge(self):
        self.ai = 2
        direction_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            counter = 0
            direction = random.randint(0, 3)
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 10 * self.size ** 2:
                if counter == 0:
                    if position.walls[direction_order[direction][0]]:
                        if not position.walls[direction_order[(direction + 3) % 4][0]]:
                            direction = (direction + 3) % 4
                            counter -= 1
                        elif not position.walls[direction_order[(direction + 2) % 4][0]]:
                            direction = (direction + 2) % 4
                            counter -= 2
                        else:
                            direction = (direction + 1) % 4
                            counter -= 3
                else:
                    if not position.walls[direction_order[(direction + 1) % 4][0]]:
                        direction = (direction + 1) % 4
                        counter += 1
                    elif not position.walls[direction_order[direction][0]]:
                        pass
                    elif not position.walls[direction_order[(direction + 3) % 4][0]]:
                        direction = (direction + 3) % 4
                        counter -= 1
                    else:
                        direction = (direction + 2) % 4
                        counter -= 2
                position = self.cells[position.x + direction_order[direction][1]][position.y + direction_order[direction][2]]
                position.visited += 1
                self.moves += 1
            if self.moves < 10 * self.size ** 2:
                break

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
