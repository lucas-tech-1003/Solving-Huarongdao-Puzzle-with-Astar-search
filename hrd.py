from __future__ import annotations

from sys import argv
from typing import List, Optional, Set


class Puzzle:
    """
    A huarongdao puzzle. 5x4 puzzle

    === Private attributes ===
    _grid: the grid representing this puzzle; each sublist contains information
        of the
    """
    _rows: int
    _cols: int
    _grid: List[List[str]]

    def __init__(self, rows: int, columns: int, grid: List[List[str]]) -> None:
        self._rows, self._cols, self._grid = rows, columns, grid

    def __str__(self) -> str:
        """
        Return a human-readable string representation of this puzzle.

        >>> r1 = ["2", "1", "1", "3"]
        >>> r2 = ["2", "1", "1", "3"]
        >>> r3 = ["4", "6", "6", "5"]
        >>> r4 = ["4", "7", "7", "5"]
        >>> r5 = ["7", "0", "0", "7"]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> print(puzzle)
        2113
        2113
        4665
        4775
        7007
        """
        # s = ""
        #
        # for row in self._grid:
        #     for col in row:
        #         s += col
        #     s += '\n'
        # return s.rstrip()

    def is_solved(self) -> bool:
        """
        Return True if this puzzle is solved. Otherwise, return False.

        >>> r1 = ["2", "6", "6", "3"]
        >>> r2 = ["2", "7", "7", "3"]
        >>> r3 = ["4", "0", "0", "5"]
        >>> r4 = ["4", "1", "1", "5"]
        >>> r5 = ["7", "1", "1", "7"]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle.is_solved()
        True

        >>> r1 = ["2", "6", "6", "3"]
        >>> r2 = ["2", "7", "7", "3"]
        >>> r3 = ["4", "1", "1", "5"]
        >>> r4 = ["4", "1", "1", "5"]
        >>> r5 = ["7", "0", "0", "7"]

        >>> puzzle = Puzzle(5, 4, [r1, r2, r3, r4, r5])
        >>> puzzle.is_solved()
        False
        """
        return self._grid[self._rows - 1][1] == "1" and \
               self._grid[self._rows - 1][2] == "1"

    def extensions(self) -> List[Puzzle]:
        pass


class Solver:
    """
    A solver for solving the huarongdao puzzle. This is an abstract class
    and only provides the interface for our solve method.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        :param puzzle: the huarongdao puzzle.
        :param seen:
        :return:
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

    def solve(self, puzzle: Puzzle, seen: Optional[Set[str]] = None) -> \
            List[Puzzle]:
        pass


def from_input_to_puzzle(input_file) -> Puzzle:
    initialGrid = []
    lines = input_file.readlines()
    for i in range(5):
        initialGrid.append([])
        for item in lines[i].strip():
            initialGrid[i].append(item)
    print(initialGrid)

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
                if i < 4 and initialGrid[i+1][j] == tile:
                    # a vertical tile 2x1
                    puzzle_rep[1].append(coord)
                else:
                    # a horizontal tile 1x2
                    puzzle_rep[2].append(coord)
    print(puzzle_rep)
    return Puzzle(5, 4, puzzle_rep)


if __name__ == "__main__":
    input_f = open(argv[1], 'r')
    # dfs_output = open(argv[2], 'w')
    # astar_output = open(argv[3], 'w')


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
