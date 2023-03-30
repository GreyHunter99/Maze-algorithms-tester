import random
from cell import *


class Maze:
    """ Maze class """
    def __init__(self, size, generation, loops):
        self.size = size
        self.generation = generation
        self.loops = loops
        self.ai = ''
        self.spawn = self.choose_spawn()
        self.end = self.choose_end()
        self.moves = 0
        self.cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        if self.generation == 0:
            self.recursive_backtracker()
        elif self.generation == 1:
            self.kruskal()
        elif self.generation == 2:
            self.prim()
        elif self.generation == 3:
            self.wilson()
        if self.loops:
            self.remove_random_walls()
        self.clear()

    def recursive_backtracker(self):
        current_cell = random.choice(random.choice(self.cells))
        current_cell.visited = True
        cell_stack = [current_cell]
        directions_order = ['top', 'right', 'bottom', 'left']
        while True:
            neighbours = dict()
            if current_cell.y < self.size - 1 and not self.cells[current_cell.x][current_cell.y + 1].visited:
                neighbours[0] = self.cells[current_cell.x][current_cell.y + 1]
            if current_cell.x < self.size - 1 and not self.cells[current_cell.x + 1][current_cell.y].visited:
                neighbours[1] = self.cells[current_cell.x + 1][current_cell.y]
            if current_cell.y > 0 and not self.cells[current_cell.x][current_cell.y - 1].visited:
                neighbours[2] = self.cells[current_cell.x][current_cell.y - 1]
            if current_cell.x > 0 and not self.cells[current_cell.x - 1][current_cell.y].visited:
                neighbours[3] = self.cells[current_cell.x - 1][current_cell.y]
            if len(neighbours) > 0:
                chosen_neighbour = random.choice(list(neighbours.items()))
                current_cell.walls[directions_order[chosen_neighbour[0]]] = False
                chosen_neighbour[1].walls[directions_order[(chosen_neighbour[0] + 2) % 4]] = False
                current_cell = chosen_neighbour[1]
                current_cell.visited = True
                cell_stack.append(current_cell)
            else:
                cell_stack.pop()
                if len(cell_stack) > 0:
                    current_cell = cell_stack[-1]
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
        cell = random.choice(random.choice(self.cells))
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

    def wilson(self):
        first_cell = random.choice(random.choice(self.cells))
        first_cell.visited = True
        directions_order = ['top', 'right', 'bottom', 'left']
        while not_visited_cells := [cell for cell_row in self.cells for cell in cell_row if not cell.visited]:
            current_cell = random.choice(not_visited_cells)
            cell_stack = [((current_cell.x, current_cell.y), [])]
            while True:
                neighbours = dict()
                if current_cell.y < self.size - 1:
                    neighbours[0] = self.cells[current_cell.x][current_cell.y + 1]
                if current_cell.x < self.size - 1:
                    neighbours[1] = self.cells[current_cell.x + 1][current_cell.y]
                if current_cell.y > 0:
                    neighbours[2] = self.cells[current_cell.x][current_cell.y - 1]
                if current_cell.x > 0:
                    neighbours[3] = self.cells[current_cell.x - 1][current_cell.y]
                chosen_neighbour = random.choice(list(neighbours.items()))
                if chosen_neighbour_in_stack := [cell_stack.index(cell) for cell in cell_stack if (chosen_neighbour[1].x, chosen_neighbour[1].y) in cell]:
                    cell_stack = cell_stack[:chosen_neighbour_in_stack[0] + 1]
                    cell_stack[-1][1].pop()
                    current_cell = chosen_neighbour[1]
                elif chosen_neighbour[1].visited:
                    chosen_neighbour[1].walls[directions_order[(chosen_neighbour[0] + 2) % 4]] = False
                    cell_stack[-1][1].append(chosen_neighbour[0])
                    for cell in cell_stack:
                        self.cells[cell[0][0]][cell[0][1]].visited = True
                        for wall in cell[1]:
                            self.cells[cell[0][0]][cell[0][1]].walls[directions_order[wall]] = False
                    break
                else:
                    current_cell = chosen_neighbour[1]
                    cell_stack[-1][1].append(chosen_neighbour[0])
                    cell_stack.append(((current_cell.x, current_cell.y), [(chosen_neighbour[0] + 2) % 4]))

    def random_mouse(self):
        self.ai = 0
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 20 * self.size ** 2:
                neighbours = []
                if not position.walls['top']:
                    neighbours.append(self.cells[position.x][position.y + 1])
                if not position.walls['bottom']:
                    neighbours.append(self.cells[position.x][position.y - 1])
                if not position.walls['left']:
                    neighbours.append(self.cells[position.x - 1][position.y])
                if not position.walls['right']:
                    neighbours.append(self.cells[position.x + 1][position.y])
                #if not_visited_neighbours := [cell for cell in neighbours if not cell.visited]:
                #    position = random.choice(not_visited_neighbours)
                #else:
                #    position = random.choice(neighbours)
                position = random.choice([cell for cell in neighbours if cell.visited == min(neighbours, key=lambda cell: cell.visited).visited])
                position.visited += 1
                self.moves += 1
            if self.moves < 20 * self.size ** 2:
                break

    def wall_follower(self):
        self.ai = 1
        mode_list = [0, 2, '']
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            mode = 0
            cell_list = [(position.x, position.y)]
            direction = random.randint(0, 3)
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 30 * self.size ** 2:
                if self.moves > 2 * self.size ** 2 and self.moves % (self.size ** 2 // 2) == 0 or self.moves > 3 * self.size ** 2 and self.moves % (self.size ** 2 // 3) == 0:
                    mode = (mode + 1) % 3
                    cell_list = [(position.x, position.y)]
                    direction = random.randint(0, 3)
                if mode == 2:
                    if position.walls[directions_order[direction][0]]:
                        mode = 0
                        cell_list = [(position.x, position.y)]
                        direction = random.randint(0, 3)
                        continue
                else:
                    if not position.walls[directions_order[(direction + 1 + mode_list[mode]) % 4][0]]:
                        direction = (direction + 1 + mode_list[mode]) % 4
                    elif not position.walls[directions_order[direction][0]]:
                        pass
                    elif not position.walls[directions_order[(direction + 3 + mode_list[mode]) % 4][0]]:
                        direction = (direction + 3 + mode_list[mode]) % 4
                    else:
                        direction = (direction + 2) % 4
                next_x = position.x + directions_order[direction][1]
                next_y = position.y + directions_order[direction][2]
                if mode != 2 and cell_list.count((next_x, next_y)) > 3:
                    mode = (mode + 1) % 3
                    cell_list = [(position.x, position.y)]
                    direction = random.randint(0, 3)
                    continue
                position = self.cells[next_x][next_y]
                position.visited += 1
                cell_list.append((position.x, position.y))
                self.moves += 1
            if self.moves < 30 * self.size ** 2:
                break

    def pledge(self):
        self.ai = 2
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            counter = 0
            direction = random.randint(0, 3)
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 10 * self.size ** 2:
                if counter == 0:
                    if position.walls[directions_order[direction][0]]:
                        if not position.walls[directions_order[(direction + 3) % 4][0]]:
                            direction = (direction + 3) % 4
                            counter -= 1
                        elif not position.walls[directions_order[(direction + 2) % 4][0]]:
                            direction = (direction + 2) % 4
                            counter -= 2
                        else:
                            direction = (direction + 1) % 4
                            counter -= 3
                else:
                    if not position.walls[directions_order[(direction + 1) % 4][0]]:
                        direction = (direction + 1) % 4
                        counter += 1
                    elif not position.walls[directions_order[direction][0]]:
                        pass
                    elif not position.walls[directions_order[(direction + 3) % 4][0]]:
                        direction = (direction + 3) % 4
                        counter -= 1
                    else:
                        direction = (direction + 2) % 4
                        counter -= 2
                position = self.cells[position.x + directions_order[direction][1]][position.y + directions_order[direction][2]]
                position.visited += 1
                self.moves += 1
            if self.moves < 10 * self.size ** 2:
                break

    def tremaux(self):
        self.ai = 3
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            direction = random.randint(0, 3)
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 30 * self.size ** 2:
                neighbours = {}
                if not position.walls['top']:
                    neighbours[0] = self.cells[position.x][position.y + 1]
                if not position.walls['right']:
                    neighbours[1] = self.cells[position.x + 1][position.y]
                if not position.walls['bottom']:
                    neighbours[2] = self.cells[position.x][position.y - 1]
                if not position.walls['left']:
                    neighbours[3] = self.cells[position.x - 1][position.y]
                if len(neighbours) > 2 or position.walls[directions_order[direction][0]]:
                    not_visited_neighbours = {cell[0]: cell[1] for cell in neighbours.items() if not cell[1].visited}
                    if not_visited_neighbours and len(neighbours) - len(not_visited_neighbours) < 2:
                        chosen_neighbour = random.choice(list(not_visited_neighbours.items()))
                        direction = chosen_neighbour[0]
                        position = chosen_neighbour[1]
                    elif (direction + 2) % 4 in {cell[0]: cell[1] for cell in neighbours.items() if cell[1].visited < 2}:
                        direction = (direction + 2) % 4
                        position = neighbours[direction]
                    else:
                        chosen_neighbour = random.choice([neighbour for neighbour in neighbours.items() if neighbour[1].visited == min(neighbours.values(), key=lambda cell: cell.visited).visited])
                        direction = chosen_neighbour[0]
                        position = chosen_neighbour[1]
                else:
                    position = neighbours[direction]
                position.visited += 1
                self.moves += 1
            if self.moves < 30 * self.size ** 2:
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
