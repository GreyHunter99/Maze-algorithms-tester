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
            self.recursive_backtracker_generation()
        elif self.generation == 1:
            self.kruskal()
        elif self.generation == 2:
            self.prim()
        elif self.generation == 3:
            self.wilson()
        elif self.generation == 4:
            self.eller()
        if self.loops:
            self.remove_random_walls()
        self.clear()

    def recursive_backtracker_generation(self):
        cell_stack = [random.choice(random.choice(self.cells))]
        cell_stack[0].visited = True
        directions_order = ['top', 'right', 'bottom', 'left']
        while len(cell_stack):
            current_cell = cell_stack[-1]
            neighbours = dict()
            if current_cell.y < self.size - 1 and not self.cells[current_cell.x][current_cell.y + 1].visited:
                neighbours[0] = self.cells[current_cell.x][current_cell.y + 1]
            if current_cell.x < self.size - 1 and not self.cells[current_cell.x + 1][current_cell.y].visited:
                neighbours[1] = self.cells[current_cell.x + 1][current_cell.y]
            if current_cell.y > 0 and not self.cells[current_cell.x][current_cell.y - 1].visited:
                neighbours[2] = self.cells[current_cell.x][current_cell.y - 1]
            if current_cell.x > 0 and not self.cells[current_cell.x - 1][current_cell.y].visited:
                neighbours[3] = self.cells[current_cell.x - 1][current_cell.y]
            if len(neighbours):
                chosen_neighbour = random.choice(list(neighbours.items()))
                current_cell.walls[directions_order[chosen_neighbour[0]]] = False
                chosen_neighbour[1].walls[directions_order[(chosen_neighbour[0] + 2) % 4]] = False
                chosen_neighbour[1].visited = True
                cell_stack.append(chosen_neighbour[1])
            else:
                cell_stack.pop()

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
            ids = []
            for index, group in enumerate(groups_of_cells):
                if wall[0] in group:
                    ids.append(index)
                if wall[1] in group:
                    ids.append(index)
                if len(ids) > 1:
                    break
            if ids[0] != ids[1]:
                groups_of_cells[ids[0]].update(groups_of_cells[ids[1]])
                del groups_of_cells[ids[1]]
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
                neighbours = {}
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

    def eller(self):
        groups_of_cells = []
        for x in range(self.size):
            for y in range(self.size):
                if self.cells[x][y].walls['left']:
                    groups_of_cells.append({(x, y)})
            if x < self.size - 1:
                for wall in range(self.size * 3 // 4 + 1):
                    y = random.randrange(self.size - 1)
                    ids = []
                    for index, group in enumerate(groups_of_cells):
                        if (x, y) in group:
                            ids.append(index)
                        if (x, y + 1) in group:
                            ids.append(index)
                        if len(ids) > 1:
                            break
                    if ids[0] != ids[1]:
                        groups_of_cells[ids[0]].update(groups_of_cells[ids[1]])
                        del groups_of_cells[ids[1]]
                        self.cells[x][y].walls['top'] = False
                        self.cells[x][y + 1].walls['bottom'] = False
                for group in groups_of_cells:
                    passage_cells = [cell for cell in group if cell[0] == x]
                    for cell in random.choices(passage_cells, k=random.randint(1, len(passage_cells))):
                        self.cells[x][cell[1]].walls['right'] = False
                        self.cells[x + 1][cell[1]].walls['left'] = False
                        group.add((x + 1, cell[1]))
            else:
                while len(groups_of_cells) > 1:
                    isolated_cells = []
                    for y in range(self.size - 1):
                        ids = []
                        for index, group in enumerate(groups_of_cells):
                            if (x, y) in group:
                                ids.append(index)
                            if (x, y + 1) in group:
                                ids.append(index)
                            if len(ids) == 2:
                                break
                        if ids[0] != ids[1]:
                            isolated_cells.append((y, ids[0], ids[1]))
                    chosen_cell = random.choice(isolated_cells)
                    groups_of_cells[chosen_cell[1]].update(groups_of_cells[chosen_cell[2]])
                    del groups_of_cells[chosen_cell[2]]
                    self.cells[x][chosen_cell[0]].walls['top'] = False
                    self.cells[x][chosen_cell[0] + 1].walls['bottom'] = False

    def random_mouse(self):
        self.ai = 0
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 20 * self.size ** 2:
                neighbours = []
                for direction in directions_order:
                    if not position.walls[direction[0]]:
                        neighbours.append(self.cells[position.x + direction[1]][position.y + direction[2]])
                position = random.choice([neighbour for neighbour in neighbours if neighbour.visited == min(neighbours, key=lambda cell: cell.visited).visited])
                position.visited += 1
                self.moves += 1
            if self.moves < 20 * self.size ** 2:
                break

    def wall_follower(self):
        self.ai = 1
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            direction = random.randint(0, 3)
            mode = random.choice([0, 2])
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 20 * self.size ** 2:
                if not position.walls[directions_order[(direction + 1 + mode) % 4][0]]:
                    direction = (direction + 1 + mode) % 4
                elif not position.walls[directions_order[direction][0]]:
                    pass
                elif not position.walls[directions_order[(direction + 3 + mode) % 4][0]]:
                    direction = (direction + 3 + mode) % 4
                else:
                    direction = (direction + 2) % 4
                next_position = self.cells[position.x + directions_order[direction][1]][position.y + directions_order[direction][2]]
                if next_position.visited:
                    neighbours = {}
                    for target in range(4):
                        if not position.walls[directions_order[target][0]] and self.cells[position.x + directions_order[target][1]][position.y + directions_order[target][2]].visited < next_position.visited:
                            neighbours[target] = self.cells[position.x + directions_order[target][1]][position.y + directions_order[target][2]]
                    if neighbours:
                        chosen_neighbour = random.choice([neighbour for neighbour in neighbours.items() if neighbour[1].visited == min(neighbours.values(), key=lambda cell: cell.visited).visited])
                        next_position = chosen_neighbour[1]
                        direction = chosen_neighbour[0]
                        mode = random.choice([0, 2])
                position = next_position
                position.visited += 1
                self.moves += 1
            if self.moves < 20 * self.size ** 2:
                break

    def pledge(self):
        self.ai = 2
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            direction = random.randint(0, 3)
            counter = 0
            mode = random.choice([0, 2])
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 10 * self.size ** 2:
                if counter == 0:
                    if position.walls[directions_order[direction][0]]:
                        if not position.walls[directions_order[(direction + 3 + mode) % 4][0]]:
                            direction = (direction + 3 + mode) % 4
                            counter -= 1
                        elif not position.walls[directions_order[(direction + 2) % 4][0]]:
                            direction = (direction + 2) % 4
                            counter -= 2
                        else:
                            direction = (direction + 1 + mode) % 4
                            counter -= 3
                else:
                    if not position.walls[directions_order[(direction + 1 + mode) % 4][0]]:
                        direction = (direction + 1 + mode) % 4
                        counter += 1
                    elif not position.walls[directions_order[direction][0]]:
                        pass
                    elif not position.walls[directions_order[(direction + 3 + mode) % 4][0]]:
                        direction = (direction + 3 + mode) % 4
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
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 20 * self.size ** 2:
                neighbours = {}
                for target in range(4):
                    if not position.walls[directions_order[target][0]]:
                        neighbours[target] = self.cells[position.x + directions_order[target][1]][position.y + directions_order[target][2]]
                if len(neighbours) > 2 or position.walls[directions_order[direction][0]]:
                    min_visited_neighbours = [neighbour[0] for neighbour in neighbours.items() if neighbour[1].visited == min(neighbours.values(), key=lambda cell: cell.visited).visited]
                    if len(neighbours) - len(min_visited_neighbours) > 1 and neighbours[(direction + 2) % 4].visited < 2:
                        direction = (direction + 2) % 4
                    else:
                        direction = random.choice(min_visited_neighbours)
                position = neighbours[direction]
                position.visited += 1
                self.moves += 1
            if self.moves < 20 * self.size ** 2:
                break

    def recursive_backtracker_solving(self):
        self.ai = 4
        directions_order = [('top', 0, 1), ('right', 1, 0), ('bottom', 0, -1), ('left', -1, 0)]
        while True:
            self.clear()
            position = self.cells[self.spawn[0]][self.spawn[1]]
            position.visited += 1
            cell_stack = [position]
            while position != self.cells[self.end[0]][self.end[1]] and self.moves < 20 * self.size ** 2:
                neighbours = []
                for direction in directions_order:
                    if not position.walls[direction[0]]:
                        neighbour = self.cells[position.x + direction[1]][position.y + direction[2]]
                        if not neighbour.visited:
                            neighbours.append(neighbour)
                if len(neighbours):
                    cell_stack.append(random.choice(neighbours))
                else:
                    cell_stack.pop()
                position = cell_stack[-1]
                position.visited += 1
                self.moves += 1
            if self.moves < 20 * self.size ** 2:
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
