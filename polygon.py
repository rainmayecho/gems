from util import sign

class Polygon(object):
    def __init__(self):
        pass

    def maximum_cosine(self, p, points):
        m = 0
        target = None
        for o in points[:-1]:
            if p == o:
                continue
            mag = (o[0] - p[0])**2 + (o[1] - p[1])**2
            dot = o[0]*1 + o[1]*0
            cos = dot*1.0 / mag
            if cos > m:
                m = cos
                target = o
        if not target:
            return points[0]
        return target

    def build(self, grid, s, t):
        v0, v1 = t[0] - s[0], t[1] - s[1]
        i, j = s
        grid[i][j] = 1
        while v0 or v1:  # remaining components of the vector
            print i, j
            prev = i, j
            if v0:  # increment position, decrement vector component
              i += sign(v0)
              v0 += -sign(v0)
            if v1:
              j += sign(v1)
              v1 += -sign(v1)
            if grid[i][j] in [2, -1]: # if position is unbuildable, repel in vector favoring direction
                i, j = prev  # revert
                if abs(v0) > abs(v1):
                    i += sign(v0)
                    v0 += -sign(v0)
                else:
                    j += sign(v1)
                    v1 += -sign(v1)

            grid[i][j] = 1

        return grid


    def offset(self, p, points):
        J = map(lambda x: x[1], points)
        I = map(lambda x: x[0], points)
        print J, I, p
        i, j = (0, 0)
        if p[1] == min(J):
            j -= 1
        if p[1] == max(J):
            j += 1
        if p[0] == min(I):
            i -= 1
        if p[0] == max(I):
            i += 1
        return (i, j)


    def construct(self, grid, checkpoints):
        s = checkpoints.pop(0)
        _all = checkpoints
        first = True
        _all.append(s)
        while _all:
            t = self.maximum_cosine(s, _all)
            if first:
                s_off = self.offset(s, _all)
                first = False
            else:
                s_off = (0, 0)
            t_off = self.offset(t, _all)
            print 'start_point = %s, %s' %((s[0] + s_off[0], s[1] + s_off[1]))
            print 'end_point = %s, %s' %((t[0] + t_off[0], t[1] + t_off[1]))
            print s_off
            grid = self.build(grid, (s[0] + s_off[0], s[1] + s_off[1]), (t[0] + t_off[0], t[1] + t_off[1]))
            s = (t[0] + t_off[0], t[1] + t_off[1])
            _all.remove(t)
        return grid


