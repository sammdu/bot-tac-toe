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


################################################################################
# Tic Tac Toe game representation
################################################################################

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


class GameState():
    """
    a class representing a Tic Tac Toe game state
    """
    next_player: str

    # Private Instance Attributes:
    #   - _board: a nested list representing a tictactoe board
    #   - _move_count: the number of moves that have been made in the current game
    _board: list[list[str]]
    _board_side: int
    _move_count: int


    def __init__(self, board: list[list[str]], next_player='p1', move_count=0) -> None:
        self._board = board
        self._board_side = len(self._board)  # calculate the side length of the game board
        self.next_player = next_player
        self._move_count = move_count

    def place_piece(self, piece: str, spot: str) -> None:
        """
        place the given piece on the given spot on the game board, if the spot is empty;
        ensure that the spot given exists on the board (is not out of range)

        Preconditions:
            - `spot` must be a string of two integers, first representing the row, second
              representing the column in the board. `ValueError`s will be raised if this
              is not satisfied
            - the spot must be empty, or a `ValueError` will be raised
            - piece in {'x', 'o'}
        """
        row = int(spot[0])
        col = int(spot[1])

        if row > self._board_side or row < 0:
            raise ValueError(f"[!] Given row {row} in spot {spot} is out of range.")
        if col > self._board_side or col < 0:
            raise ValueError(f"[!] Given column {col} in spot {spot} is out of range.")

        if not self._board[row][col]:  # check if the spot is empty
            self._board[row][col] = piece
        else:
            raise ValueError(f"[!] Given spot {spot} is not empty.")


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

        # grab the side length fo the game board
        side = self._board_side

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


g = GameState(empty_board(3))
g.place_piece('x', '22')
print(g._board)
g.get_winner()


################################################################################
# Player Classes
################################################################################
class Player:
    """
    An abstract class representing a Tic Tac Toe player.
    """
    # Private Instance Attributes:
    #   - _piece: game piece of the current player, either `x` or `o`
    _piece: str

    def __init__(self, piece) -> None:
        assert piece in {'x', 'o'}
        self._piece = piece

    def make_move(self, game: GameState, prev_move: str, your_move=None):
        """
        Make a move in the given game state.

        `prev_move` is the opponent player's most recent move, or `None` if no moves
        have been made
        `your_move` is only used by a human player, to supply a move to make; an AI player
        will disregard this argument
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """
    A human player who takes a given
    """


class AIRandomPlayer(Player):
    """
    """


class AIMinimaxPlayer(Player):
    """
    """


if __name__ == '__main__':
    import doctest
    doctest.testmod()
