def sign(n):
    if n < 0:
        return -1
    if n > 0:
        return 1
    if n == 0:
        return 0

def flatten(l):
    return [item for sublist in l for item in sublist]

def m_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1]  - b[1])

def expand(G, i, j, path, early=True):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    res = []
    for d in dirs:
        try:
            _i = i + d[0]
            _j = j + d[1]
            if _i < 0 or _j < 0:
                continue
            x = G[_i][_j]
            if x not in [1, -1] and path[_i][_j] == 0:
                res.append((_i, _j))
                path[_i][_j] = (i, j)
        except IndexError:
            continue
    return res, path

def resolve_path(path, v, w):
    p = [w]
    cur = w
    try:
        while cur != v:
            i, j = cur
            n = path[i][j]
            p.append(n)
            cur = n
    except Exception as e:
        raise InvalidPlacement
    return p

def A_star(G, v, w):
    q = [v]
    path = [[0 for j in xrange(37)] for i in xrange(37)]
    while q:
        i, j = q.pop(0)
        if (i, j) == w:
            ret = resolve_path(path, v, w)
#             print '%s --> %s: %s' %(v, w, len(ret))
            return ret
        res, p = expand(G, i, j, path)
        q.extend(res)
        path = p
    ret = resolve_path(path, v, w)
    print '%s --> %s: %s' %(v, w, len(ret))
    return ret


class InvalidPlacement(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Invalid Placement. A* cannot find a solution.'
