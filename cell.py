class Cell:
    """ Cell class """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'bottom': True, 'left': True, 'right': True}
        self.visited = False
