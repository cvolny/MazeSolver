from copy import deepcopy
from functools import lru_cache
from os import system, name
from time import sleep


VERBOSE = False
VALUE_WALL = "#"
VALUE_VISITED = "@"
VALUE_OPEN = " "
VALUE_START = "S"
VALUE_FINISH = "F"


def cls():
    system(['clear', 'cls'][name == 'nt'])


def readfile(filename):

    filedata = None
    with open(filename) as f:
        filedata = f.read().splitlines()

    assert(None != filedata)
    return filedata


def parsemaze(data):
    columns = None
    start = None
    finish = None
    r = 0
    table = []
    for line in data:
        ldata = list(line)

        if not ldata:
            break
        if None == columns:
            columns = len(ldata)
        else:
            assert(len(ldata) == columns)

        try:
            while True:
                sc = ldata.index(VALUE_START)
                assert(None == start)
                start = (r, sc)
                ldata[sc] = VALUE_OPEN
        except ValueError:
            pass

        fset = False
        try:
            while True:
                sf = ldata.index(VALUE_FINISH)
                assert(None == finish)
                finish = (r, sf)
                fset = True
                ldata[sf] = VALUE_OPEN
        except ValueError:
            if fset:
                ldata[sf] = VALUE_FINISH

        table.append(ldata)
        r += 1

    assert(not None == start)
    assert(not None == finish)

    return table, start, finish


def boundaries(maze):
    return _boundaries(len(maze), len(maze[0]))


@lru_cache(maxsize=2)
def _boundaries(r, c):
    return (0, r), (0, c)


def inside(maze, y, x):
    (ymin, ymax), (xmin, xmax) = boundaries(maze)
    if not xmin < x < xmax:
        return False
    if not ymin < y < ymax:
        return False
    return True


def nextmoves(y, x):
        yield y, x - 1
        yield y, x + 1
        yield y - 1, x
        yield y + 1, x


def printer(maze, current, target, delay):
    if VERBOSE:
        cls()
        for line in maze:
            print(''.join(line))
        sleep(delay)


def solver(maze, current, target):
    y, x = current

    if target == current:
        return True

    if not inside(maze, y, x):
        return False

    if not maze[y][x] in (VALUE_OPEN, VALUE_START):
        return False

    maze[y][x] = VALUE_VISITED
    printer(maze, current, target, 0.10)

    for move in nextmoves(y, x):
        if solver(deepcopy(maze), move, target):
            return True
    return False


def main(mazefile):
    maze, start, finish = parsemaze(readfile(mazefile))
    solveable = solver(maze, start, finish)
    if solveable:
        print("Pretty Easy!")
    else:
        print("Cheater!")


if "__main__" == __name__:
    VERBOSE = True
    main("maze2.txt")