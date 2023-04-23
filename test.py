from maze import *


class Test:
    """ Test class """
    def __init__(self, number_of_mazes, number_of_solutions, size, generations, ais):
        self.number_of_mazes = number_of_mazes
        self.number_of_solutions = number_of_solutions
        self.size = size
        self.generations = generations
        self.ais = ais
        self.loops = False
        self.results = {}
        self.stats = {}

    def testing(self):
        for generation in self.generations:
            generation = int(generation)
            self.results[generation] = []
            self.stats[generation] = {}
            for ai_id in self.ais:
                self.stats[generation][int(ai_id)] = {'moves': []}
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
                        if ai == 2:
                            maze.pledge()
                        if ai == 3:
                            maze.tremaux()
                        if ai == 4:
                            maze.recursive_backtracker_solving()
                        self.results[generation][i][ai].append(maze.moves)
                    self.results[generation][i][ai].sort()
                    self.stats[generation][ai]['moves'].extend(self.results[generation][i][ai])
            for ai_id in self.ais:
                self.stats[generation][int(ai_id)]['len'] = len(self.stats[generation][int(ai_id)]['moves'])
                self.stats[generation][int(ai_id)]['max'] = max(self.stats[generation][int(ai_id)]['moves'])
                self.stats[generation][int(ai_id)]['min'] = min(self.stats[generation][int(ai_id)]['moves'])
                self.stats[generation][int(ai_id)]['moves'].sort()
                self.stats[generation][int(ai_id)]['med'] = (self.stats[generation][int(ai_id)]['moves'][self.stats[generation][int(ai_id)]['len'] // 2] + self.stats[generation][int(ai_id)]['moves'][- (self.stats[generation][int(ai_id)]['len'] // 2) - 1]) / 2
                self.stats[generation][int(ai_id)]['moves'] = sum(self.stats[generation][int(ai_id)]['moves'])
                self.stats[generation][int(ai_id)]['avg'] = round(self.stats[generation][int(ai_id)]['moves'] / (self.number_of_mazes * self.number_of_solutions), 2)
