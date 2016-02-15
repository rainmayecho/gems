import Tkinter
import Image, ImageTk, ImageDraw
import os, sys
import cStringIO, base64
from util import *
from optimizer import OptimizingFunction
from decision import *

class MazeGenerator(object):


    def __init__(self):
        self.grid = []
        self.paths = []
        self.SIZE = 1000
        self.NODE_COUNT = 5
        self.im = Image.new('RGB', (self.SIZE, self.SIZE))
        self.draw = ImageDraw.Draw(self.im)
        self.init_maze()
        self.H = []
        self._heat_map()
        self.prev_build_loc = None
        self.functions = {}
        self.set_optimizing_functions()

    def init_maze(self):
        self.grid = [list([0]*37) for i in xrange(37)]
        for row in xrange(37):
            for col in xrange(37):
                if row < 7 and col < 7:
                    self.grid[row][col] = -1
                if row > 29 and col > 29:
                    self.grid[row][col] = -1
        self.grid[18][4] = 2
        self.grid[18][32] = 2
        self.grid[4][32] = 2
        self.grid[4][18] = 2
        self.grid[32][18] = 2

    def set_optimizing_functions(self):
      # Maximize Path Length
      self.functions['path'] = (OptimizingFunction(None, len, 'gte'))

      # Maximize central surface area
      central = flatten([[(i, j) for j in xrange(self.SIZE)] for i in xrange(self.SIZE)])
      center = (18, 18)
      central = set(filter(lambda p: m_dist(p, center) <= 7, central))
      self.functions['area'] = OptimizingFunction(None, set.intersection_update, 'gte', function_parameter='center', function_metric=len, center=central)


    def _heat_map(self):
        self.H = [list([0]*37) for i in xrange(37)]
        mid = 37/2
        for row in xrange(37):
            for col in xrange(37):
                if self.grid[row][col] in [-1, 2]:
                    self.H[row][col] = 38
                else:
                    self.H[row][col] = abs(mid - row) + abs(mid - col)
                    if row == mid:
                        self.H[row][col] -= 1
                    if col == mid:
                        self.H[row][col] -= 1

    def connectivity(self):
        _st_pairs = [((7, 4), (18, 4)), ((18, 4), (18, 32)), ((18, 32), (4, 32)), ((4, 32), (4, 18)), ((4, 18), (32, 18)), ((32, 18), (32, 29))]
        flat_pairs = flatten(_st_pairs)
        collisions = {}
        for v, w in _st_pairs:
            path = A_star(self.grid, v, w)
            self.paths.append(path)
            if path == 'INVALID':
              pi, pj = self.prev_build_loc
              self.grid[pi][pj] = 0
              self.H[pi][pj] = 1000000
            for p in path:
                i, j = p
                if self.grid[i][j] in [1, -1, 2]:
                    continue
                try:
                    collisions[p] -= self.H[i][j]
                except KeyError:
                    collisions[p] = self.H[i][j]
        return sorted(collisions.items(), key = lambda x: x[1])

    def get_path(self):
      path = []
      for p in self.paths:
        path.extend(p[:-1])
      path.append((32, 29))
      self.path = path
      return path

    def draw_path(self):
      for p in self.get_path():
        j, i = p
        if self.grid[i][j] in [-1, 2, 1]:
          continue
        k = self.SIZE/(len(self.grid))
        i *= k
        j *= k
        self.draw.rectangle([i, j , i + k, j + k], (0, 0, 255))

    def create_frame(self):
        L = len(self.grid)
        red = (255, 0, 0)
        green = (0, 255, 0)
        k = self.SIZE/L
        for j in xrange(L):
          for i in xrange(L):
            _i = i * k
            _j = j * k
            if self.grid[j][i] == 1:
              self.draw.rectangle([_i, _j, (_i + k), (_j + k)], red)
            if self.grid[j][i] == 2:
              self.draw.rectangle([_i, _j, (_i + k), (_j + k)], green)
        self.draw_path()
        self.im.save('test.png')
        return self.im

    def clear_frame(self):
        self.paths = []
        self.draw.rectangle([0, 0, self.SIZE, self.SIZE], (0, 0, 0))


    def generate(self):
        self.clear_frame()
        DT = Tree(self.grid, self.functions)
        for i, j in DT.root.get_best_placements():
            self.grid[i][j] = 1
        return self.create_frame()


def step(event):
    f = MG.generate()
    image = ImageTk.PhotoImage(f)
    image_label.config(image=image)
    image_label.pack()


if __name__ == '__main__':
    root = Tkinter.Tk()
    root.bind("<Return>", step)
    image = None
    MG = MazeGenerator()
    image_label = Tkinter.Label(root)
    root.mainloop()

