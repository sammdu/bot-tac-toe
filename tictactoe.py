"""
The TicTacToe game class and peripheral functions.

--------------------------------------------------------------------------------
MIT License

Copyright (c) 2021 Mu "Samm" Du

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from __future__ import annotations
from typing import Optional
import random


def empty_board(side: int) -> None:
    """
    generate an empty game board (list of lists) with sidelength `side`

    >>> empty_board(3)
    [['', '', ''], ['', '', ''], ['', '', '']]
    """
    board = []
    for i in range(side):
        row = [''] * side
        board.append(row)
    return board


empty_board(3)


class GameState():
    """
    a class representing a Tic Tac Toe game state
    """
    # Private Instance Attributes:
    #   - _board: a nested list representing a tictactoe board
    #   - _move_count: the number of moves that have been made in the current game
    _board: list[list[str]]
    _move_count
    next_player: str

    def __init__(
        self,
        board: list[list[str]],
        next_player='p1',
        move_count=0
    ) -> None:
        self._board = board
        self.next_player = next_player

    def get_winner(self) -> str:
        """
        return 'x' or 'o' or `None` as the winner of the game in its current state
        """
        # check each row
        for row in self._board:
            if all(spot == 'x' for spot in row):
                return 'x'
            elif all(spot == 'o' for spot in row):
                return 'o'

        side = len(self._board)

        # if no winners in rows, check each column
        for col_num in range(side):
            if all(row[col_num] == 'x' for row in self._board):
                return 'x'
            elif all(row[col_num] == 'o' for row in self._board):
                return 'o'

        # if still no winners, check the two diagonals
        # top-left to bottom-right
        if all(self._board[i][i] == 'x' for i in range(side)):
            return 'x'
        elif all(self._board[i][i] == 'o' for i in range(side)):
            return 'o'
        # top-right to bottom-left
        if all(self._board[i][side - i - 1] == 'x' for i in range(side)):
            return 'x'
        elif all(self._board[i][side - i - 1] == 'o' for i in range(side)):
            return 'o'

        # if there are empty spots in the board then no winners yet
        # [*] this can be improved by predicting early ties, but I won't implement it
        # right now
        if not all(self._board[i][j] for i in range(side) for j in range(side)):
            return None

        # otherwise it's a tie
        return "tie"


class Player:
    """
    """

    def make_move(self):
        """
        """
        raise NotImplementedError


class HumanPlayer():
    """
    """


class AIRandomPlayer():
    """
    """


class AIMinimaxPlayer():
    """
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
