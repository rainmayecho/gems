from util import sign

class Polygon(object):
    def __init__(self):
        pass

    def maximum_cosine(self, p, points):
        m = 0
        target = None
        for o in points:
            if p == o:
                continue
            mag = (o[0] - p[0])**2 + (o[1] - p[1])**2
            dot = o[0]*1 + o[1]*0
            cos = dot*1.0 / mag
            if cos > m:
                m = cos
                target = o
        return target

    def build(self, grid, s, t):
        v0, v1 = t[0] - s[0], t[1] - s[1]
        i, j = s
        while v0 or v1:
            grid[i][j] = 1
            if v0:
              i += sign(v0)
              v0 += -sign(v0)
            if v1:
              j += sign(v1)
              v1 += -sign(v1)

        return grid


    def offset(self, p, points):
        J = map(lambda x: x[1], points)
        I = map(lambda x: x[0], points)
        if p[1] == min(J):
            return (0, -1)
        if p[1] == max(J):
            return (0, 1)
        if p[0] == min(I):
            return (-1, 0)
        if p[0] == max(I):
            return (1, 0)
        return (1, 1)


    def construct(self, grid, include, exclude):
        while include:
            s = include.pop(0)
            t = self.maximum_cosine(s, include)
            print s
            s_off = self.offset(s, include)
            t_off = self.offset(t, include)
            grid = self.build(grid, (s[0] + s_off[0], s[1] + s_off[1]), (t[0] + t_off[0], t[1] + t_off[1]))
            return grid


