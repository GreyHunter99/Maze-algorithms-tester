import random
from cell import *


class Maze:
    """ Maze class """
    def __init__(self, size):
        self.size = size
        self.end = []
        self.spawn = []
        self.moves = 0
        self.cells = self.generate_cells()

    def generate_cells(self):
        cells = [[Cell(x, y) for y in range(self.size)] for x in range(self.size)]
        edges = set()
        for x in range(self.size):
            for y in range(self.size):
                if x == 0 or x == self.size-1 or y == 0 or y == self.size-1:
                    edges.add((x, y))
        edges = list(edges)
        self.end = random.choice(edges)
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

        for x in range(int(self.size / 2 - self.size / 10), int(self.size / 2 + self.size / 10)):
            for y in range(int(self.size / 2 - self.size / 10), int(self.size / 2 + self.size / 10)):
                self.spawn.append((x, y))
        self.spawn = random.choice(self.spawn)

        for x in range(self.size):
            for y in range(self.size):
                cells[x][y].visited = 0

        return cells

    def ai(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].visited = 0

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

    def clear(self):
        for x in range(self.size):
            for y in range(self.size):
                self.cells[x][y].visited = 0
