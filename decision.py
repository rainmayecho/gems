from util import *
import time
from PIL import Image, ImageTk, ImageDraw

def next_placements(G, p):
    dirs = [(0, -1), (-1, -1), (-1, 0), (1, 0), (0, 1)]
    res = []
    i, j = p
    for d in dirs:
        try:
            _i = i + d[0]
            _j = j + d[1]
            if _i < 0 or _j < 0:
                continue
            x = G[_i][_j]
            if x not in [1, -1, 2]:
                res.append((_i, _j))
        except IndexError:
            continue
    return res

def copy(G):
    R =[]
    for row in G:
        R.append(list(row))
    return R

class TreeNode(object):
    def __init__(self, grid=None, placement=None, score=None, functions={}):
        self.grid = grid
        self.placement = placement
        self.score = score
        self.functions = functions
        self.SIZE = 1000
        self.im = Image.new('RGB', (self.SIZE, self.SIZE))
        self.draw = ImageDraw.Draw(self.im)

    def get_best_placements(self, depth=18, placements=[]):
        print 'Depth: %s' %(18-depth)
        if not depth:
            self.score = self.evaluate()
            if self.score > 20:
                return placements
            return []
        for p in next_placements(self.grid, self.placement):
            G = copy(self.grid)
            i, j = p
            G[i][j] = 1
            node = TreeNode(G, p, None, self.functions)
            node.get_best_placements(depth-1, placements+[p])
            score = max(node.score, self.evaluate())
            if score >= 1.5*(19-depth):
                return placements + [p]
        return []

    def evaluate(self):
        self.clear_frame()
        if self.score:
            return self.score
        net = 0
        for name, f in self.functions.items():
            try:
                f.target = self.get_path()
                print 'Evaluating OptimizingFunction "%s"...' %(name)
                net += f.evaluate_placement()
                print '----> Net gain: %s' %(net)
            except InvalidPlacement:
                return -10000
            time.sleep(5)
            self.create_frame()
        return net

    def get_path(self):
        _st_pairs = [((7, 4), (18, 4)), ((18, 4), (18, 32)), ((18, 32), (4, 32)), ((4, 32), (4, 18)), ((4, 18), (32, 18)), ((32, 18), (32, 29))]
        flat_pairs = flatten(_st_pairs)
        path = []
        for v, w in _st_pairs:
            p = A_star(self.grid, v, w)
            path.extend(p[:-1])
        print len(path)
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

class Tree(object):
    def __init__(self, grid, functions):
        self.root = TreeNode(grid, (18, 18), None, functions)

