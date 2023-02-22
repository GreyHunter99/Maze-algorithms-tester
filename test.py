from maze import *


class Test:
    """ Test class """
    def __init__(self, number_of_mazes, number_of_solutions, size, generations, ais, loops):
        self.number_of_mazes = number_of_mazes
        self.number_of_solutions = number_of_solutions
        self.size = size
        self.generations = generations
        self.ais = ais
        self.loops = loops
        self.results = {}
        self.avg = {}

    def testing(self):
        for generation in self.generations:
            generation = int(generation)
            self.results[generation] = []
            self.avg[generation] = {}
            for ai_id in self.ais:
                self.avg[generation][int(ai_id)] = 0
            for i in range(self.number_of_mazes):
                self.results[generation].append({})
                maze = Maze(self.size, generation, self.loops)
                for ai in self.ais:
                    ai = int(ai)
                    self.results[generation][i][ai] = []
                    for j in range(self.number_of_solutions):
                        if ai == 0:
                            maze.random_mouse()
                        if ai == 1:
                            maze.wall_follower()
                        self.results[generation][i][ai].append(maze.moves)
                        self.avg[generation][ai] += maze.moves
            for ai_id in self.ais:
                self.avg[generation][int(ai_id)] = self.avg[generation][int(ai_id)] / (self.number_of_mazes * self.number_of_solutions)
