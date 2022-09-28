from __future__ import annotations

import sys
from collections import deque
from sys import argv
from typing import List, Optional, Set, Tuple


class Puzzle:
    """
    A huarongdao puzzle that is dimensionally 5x4. There are 5 different types
    of tiles in the puzzle.

    === Private attributes ===
    _rows: the number of rows in the puzzle
    _cols: the number of columns
    _grid: the grid representing this puzzle; each sublist contains the
        information of each type of the tile in the form of a tuple, each tuple
        stores the y coordinate, x coordinate, and the name of the tile. For
        example: first sublist contains one tuple representing the 2x2 tile,
                 second sublist contains tuples of the vertical tiles,
                 third sublist contains tuples of the horizontal tiles,
                 fourth sublist contains tuples of the 1x1 tiles, and
                 fifth sublist contains tuples of the empty space
    parent: the parent of this puzzle. Defaults to None
    """
    _rows: int
    _cols: int
    _grid: List[List[Tuple[int, int, str]]]
    parent: Puzzle

    def __init__(self, rows: int, columns: int,
                 grid: List[List[Tuple[int, int, str]]],
                 parent: Optional[Puzzle] = None) -> None:
        self._rows, self._cols, self._grid = rows, columns, grid
        self.parent = parent

    def _convert_puzzle_to_list(self) -> List[List[str]]:
        """
        Convert the puzzle to a nested list of strings.

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(4, 1, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle._convert_puzzle_to_list()
        [['3', '1', '1', '3'], ['3', '1', '1', '3'], ['3', '2', '2', '3'], ['3', '4', '4', '3'], ['4', '0', '0', '4']]
        """
        lst = [["", "", "", ""],
               ["", "", "", ""],
               ["", "", "", ""],
               ["", "", "", ""],
               ["", "", "", ""]]
        cao_cao = self._grid[0][0]
        vertical = self._grid[1]
        horizontal = self._grid[2]
        soldier = self._grid[3]
        empty = self._grid[4]

        lst[cao_cao[0]][cao_cao[1]] = cao_cao[2]
        lst[cao_cao[0]][cao_cao[1] + 1] = cao_cao[2]
        lst[cao_cao[0] + 1][cao_cao[1]] = cao_cao[2]
        lst[cao_cao[0] + 1][cao_cao[1] + 1] = cao_cao[2]
        for tile in vertical:
            lst[tile[0]][tile[1]] = '3'
            lst[tile[0] + 1][tile[1]] = '3'
        for tile in horizontal:
            lst[tile[0]][tile[1]] = '2'
            lst[tile[0]][tile[1] + 1] = '2'
        for tile in soldier:
            lst[tile[0]][tile[1]] = '4'
        for tile in empty:
            lst[tile[0]][tile[1]] = '0'

        return lst

    def __str__(self) -> str:
        """
        Return a human-readable string representation of this puzzle.

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(4, 1, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> print(puzzle)
        3113
        3113
        3223
        3443
        4004
        """
        grid = self._convert_puzzle_to_list()
        s = ""
        for row in grid:
            for col in row:
                s += col
            s += '\n'
        return s.rstrip()

    def is_solved(self) -> bool:
        """
        Return True if this puzzle is solved. Otherwise, return False.

        >>> r1 = [(3, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(1, 1, '6')]
        >>> r4 = [(0, 1, '7'), (0, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(2, 1, '0'), (2, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle.is_solved()
        True

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(4, 1, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle.is_solved()
        False
        """
        cao_cao = self._grid[0][0]
        return (cao_cao[0], cao_cao[1]) == (3, 1)

    def copy_puzzle(self) -> Puzzle:
        """
        return a copy of this Puzzle

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(4, 1, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle.copy_puzzle() != puzzle
        True
        >>> puzzle.copy_puzzle()._grid == puzzle._grid
        True
        >>> print(puzzle)
        3113
        3113
        3223
        3443
        4004
        >>> print(puzzle.copy_puzzle())
        3113
        3113
        3223
        3443
        4004
        """
        grid = [[self._grid[i][j] for j in range(len(self._grid[i]))]
                for i in range(self._rows)]
        return Puzzle(self._rows, self._cols, grid)

    def _not_hit_boundary(self, y, x, direction: str) -> bool:
        """
        Return True if the tile can be moved to a direction, where direction is
        either 'N', 'W', 'S', 'E'. Otherwise, return False
        """
        if direction == 'N':
            return y != 0
        elif direction == 'S':
            return (y + 1) != self._rows
        elif direction == 'E':
            return (x + 1) != self._cols
        else:
            return x != 0

    def _move_cao_cao(self) -> List[Puzzle]:
        """
        return a list of puzzles. Each puzzle is a state after moving cao_cao
        """
        lst = []

        cao_cao = self._grid[0][0]
        empty = self._grid[4]
        empties = {(empty[0][0], empty[0][1]), (empty[1][0], empty[1][1])}
        y, x = cao_cao[0], cao_cao[1]
        if self._not_hit_boundary(y, x, 'N'):
            new_set = {(y - 1, x), (y - 1, x + 1)}
            if new_set.issubset(empties):
                puzzle = self.copy_puzzle()
                puzzle.parent = self
                # update cao_cao
                puzzle._grid[0][0] = (y - 1, x, cao_cao[2])
                # update two empty cells
                puzzle._grid[4] = [(y + 1, x, '0'), (y + 1, x + 1, '0')]
                lst.append(puzzle)
        if self._not_hit_boundary(y + 1, x, 'S'):
            new_set = {(y + 2, x), (y + 2, x + 1)}
            if new_set.issubset(empties):
                puzzle = self.copy_puzzle()
                puzzle.parent = self
                # update cao_cao
                puzzle._grid[0][0] = (y + 1, x, cao_cao[2])
                # update two empty cells
                puzzle._grid[4] = [(y, x, '0'), (y, x + 1, '0')]
                lst.append(puzzle)
        if self._not_hit_boundary(y, x + 1, 'E'):
            new_set = {(y, x + 2), (y + 1, x + 2)}
            if new_set.issubset(empties):
                puzzle = self.copy_puzzle()
                puzzle.parent = self
                # update cao_cao
                puzzle._grid[0][0] = (y, x + 1, cao_cao[2])
                # update two empty cells
                puzzle._grid[4] = [(y, x, '0'), (y + 1, x, '0')]
                lst.append(puzzle)
        if self._not_hit_boundary(y, x, 'W'):
            new_set = {(y, x - 1), (y + 1, x - 1)}
            if new_set.issubset(empties):
                puzzle = self.copy_puzzle()
                puzzle.parent = self
                # update cao_cao
                puzzle._grid[0][0] = (y, x - 1, cao_cao[2])
                # update two empty cells
                puzzle._grid[4] = [(y, x + 1, '0'), (y + 1, x + 1, '0')]
                lst.append(puzzle)
        return lst

    def _move_vertical(self) -> List[Puzzle]:
        """
        return a list of puzzles. Each puzzle is a state after moving a vertical
            tile

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(4, 1, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle._move_vertical()
        []

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 1, '7'), (4, 3, '7')]
        >>> r5 = [(4, 0, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> print(puzzle._move_vertical()[0])
        3113
        3113
        0223
        3443
        3404
        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(3, 2, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (0, 0, '7'), (4, 1, '7'), (4, 3, '7')]
        >>> r5 = [(4, 0, '0'), (1, 0, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> print(puzzle._move_vertical()[0])
        4113
        3113
        3223
        0433
        0434
        >>> print(puzzle._move_vertical()[1])
        4113
        0113
        0223
        3433
        3434
        """
        lst = []
        vertical = self._grid[1]
        empty = self._grid[4]
        empties = {(empty[0][0], empty[0][1]), (empty[1][0], empty[1][1])}

        for i in range(len(vertical)):
            y, x, name = vertical[i]
            if self._not_hit_boundary(y, x, 'N'):
                new_set = {(y - 1, x)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this vertical tile
                    puzzle._grid[1][i] = (y - 1, x, name)
                    # update the according empty tile
                    empty_now = (y + 1, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y - 1, x, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
            if self._not_hit_boundary(y + 1, x, 'S'):
                new_set = {(y + 2, x)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this vertical tile
                    puzzle._grid[1][i] = (y + 1, x, name)
                    # update the according empty tile
                    empty_now = (y, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y + 2, x, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'E'):
                new_set = {(y, x + 1), (y + 1, x + 1)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this vertical tile
                    puzzle._grid[1][i] = (y, x + 1, name)
                    # update the according empty tile
                    puzzle._grid[4] = [(y, x, '0'), (y + 1, x, '0')]
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'W'):
                new_set = {(y, x - 1), (y + 1, x - 1)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this vertical tile
                    puzzle._grid[1][i] = (y, x - 1, name)
                    # update the according empty tile
                    puzzle._grid[4] = [(y, x, '0'), (y + 1, x, '0')]
                    lst.append(puzzle)
        return lst

    def _move_horizontal(self) -> List[Puzzle]:
        """
        return a list of puzzles. Each puzzle is a state after moving a
        horizontal tile

        """
        lst = []
        horizontal = self._grid[2]
        empty = self._grid[4]
        empties = {(empty[0][0], empty[0][1]), (empty[1][0], empty[1][1])}

        for i in range(len(horizontal)):
            y, x, name = horizontal[i]
            if self._not_hit_boundary(y, x, 'N'):
                new_set = {(y - 1, x), (y - 1, x + 1)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this horizontal tile
                    puzzle._grid[2][i] = (y - 1, x, name)
                    # update the according empty tile
                    puzzle._grid[4] = [(y, x, '0'), (y, x + 1, '0')]
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'S'):
                new_set = {(y + 1, x), (y + 1, x + 1)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this horizontal tile
                    puzzle._grid[2][i] = (y + 1, x, name)
                    # update the according empty tile
                    puzzle._grid[4] = [(y, x, '0'), (y, x + 1, '0')]
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'E'):
                new_set = {(y, x + 2)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this horizontal tile
                    puzzle._grid[2][i] = (y, x + 1, name)
                    # update the according empty tile
                    empty_now = (y, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y, x + 2, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'W'):
                new_set = {(y, x - 1)}
                if new_set.issubset(empties):
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this horizontal tile
                    puzzle._grid[2][i] = (y, x - 1, name)
                    # update the according empty tile
                    empty_now = (y, x + 1, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y, x - 1, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
        return lst

    def _move_soldier(self) -> List[Puzzle]:
        """
        return a list of puzzles. Each puzzle is a state after moving soldier

        """
        lst = []
        soldier = self._grid[3]
        empty = self._grid[4]
        empties = [(empty[0][0], empty[0][1]), (empty[1][0], empty[1][1])]

        for i in range(len(soldier)):
            y, x, name = soldier[i]
            if self._not_hit_boundary(y, x, 'N'):
                if (y - 1, x) in empties:
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this 1x1 tile
                    puzzle._grid[3][i] = (y - 1, x, name)
                    # update the according empty tile
                    empty_now = (y, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y - 1, x, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'S'):
                if (y + 1, x) in empties:
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this 1x1 tile
                    puzzle._grid[3][i] = (y + 1, x, name)
                    # update the according empty tile
                    empty_now = (y, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y + 1, x, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'E'):
                if (y, x + 1) in empties:
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this 1x1 tile
                    puzzle._grid[3][i] = (y, x + 1, name)
                    # update the according empty tile
                    empty_now = (y, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y, x + 1, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
            if self._not_hit_boundary(y, x, 'W'):
                if (y, x - 1) in empties:
                    puzzle = self.copy_puzzle()
                    puzzle.parent = self
                    # update this 1x1 tile
                    puzzle._grid[3][i] = (y, x - 1, name)
                    # update the according empty tile
                    empty_now = (y, x, '0')
                    # find which empty tile is the one that moved
                    if puzzle._grid[4][0] == (y, x - 1, '0'):
                        puzzle._grid[4][0] = empty_now
                    else:
                        puzzle._grid[4][1] = empty_now
                    lst.append(puzzle)
        return lst

    def extensions(self) -> List[Puzzle]:
        """
        return a list of puzzles that is a successor of current puzzle

        >>> r1 = [(0, 1, '1')]
        >>> r2 = [(0, 0, '2'), (0, 3, '3'), (2, 0, '4'), (2, 3, '5')]
        >>> r3 = [(2, 1, '6')]
        >>> r4 = [(3, 1, '7'), (3, 2, '7'), (4, 0, '7'), (4, 3, '7')]
        >>> r5 = [(4, 1, '0'), (4, 2, '0')]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> len(puzzle.extensions())
        4
        """
        successors = []
        successors.extend(self._move_cao_cao())
        successors.extend(self._move_soldier())
        successors.extend(self._move_vertical())
        successors.extend(self._move_horizontal())

        return successors

    def get_path(self) -> List[Puzzle]:
        """
        return a list of puzzles that forms a path to the solution.
        """
        path = [self]
        parent = self.parent
        while parent is not None:
            path.append(parent)
            parent = parent.parent
        path.reverse()
        return path


class Solver:
    """
    A solver for solving the huarongdao puzzle. This is an abstract class
    and only provides the interface for our solve method.
    """

    def solve(self, puzzle: Puzzle) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        """
        raise NotImplementedError


class AStarSolver(Solver):
    """
    A solver for solving the huarongdao puzzle using the A* search technique.
    """

    def solve(self, puzzle: Puzzle, seen: Optional[Set[str]] = None) -> List[
        Puzzle]:
        pass


class DfsSolver(Solver):
    """
    A solver for solving the huarongdao puzzle using a depth-first search
    algorithm.
    """

    def solve(self, puzzle: Puzzle) -> List[Puzzle]:
        frontier = deque([puzzle])
        seen = set()
        while len(frontier) > 0:
            state = frontier.pop()
            if state not in seen:
                seen.add(str(state))
                if state.is_solved():
                    return state.get_path()
                for successor in state.extensions():
                    frontier.append(successor)
        return [puzzle]


def from_input_to_puzzle(input_file) -> Puzzle:
    initialGrid = []
    lines = input_file.readlines()
    for i in range(5):
        initialGrid.append([])
        for item in lines[i].strip():
            initialGrid[i].append(item)
    # print(initialGrid)

    puzzle_rep = [[], [], [], [], []]
    seen = set()
    for i in range(5):
        for j in range(4):
            tile = initialGrid[i][j]
            if tile in seen:
                continue
            if tile == '1':
                seen.add(tile)
                coord = (i, j, tile)
                puzzle_rep[0].append(coord)
            elif tile == '7':
                coord = (i, j, tile)
                puzzle_rep[3].append(coord)
            elif tile == '0':
                coord = (i, j, tile)
                puzzle_rep[4].append(coord)
            else:
                seen.add(tile)
                coord = (i, j, tile)
                if i < 4 and initialGrid[i + 1][j] == tile:
                    # a vertical tile 2x1
                    puzzle_rep[1].append(coord)
                else:
                    # a horizontal tile 1x2
                    puzzle_rep[2].append(coord)
    # print(puzzle_rep)
    return Puzzle(5, 4, puzzle_rep)


if __name__ == "__main__":
    input_f = open(argv[1], 'r')
    input_puzzle = from_input_to_puzzle(input_f)
    dfs_output = open(argv[2], 'w')
    # astar_output = open(argv[3], 'w')

    sys.stdout = dfs_output
    dfs_solution = DfsSolver().solve(input_puzzle)
    for item in dfs_solution:
        print(item)

# names = ["a", "b", "c"]
# ages = [12, 20, 22]
# age = 18
# older = []
# younger = []
# for i in range(len(names)):
#     if ages[i] < age:
#         younger.append(names[i])
#     elif ages[i] > age:
#         older.append(names[i])
# print(older)
# print(younger)
