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
from typing import Optional, Union
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
    A class representing a Tic Tac Toe game state.

    [c] This class took inspiration from CSC111 Winter 2021 Assignment 2: Trees, Chess,
        and Artificial Intelligence (Minichess Library), by David Liu and Isaac Waller;
        though there are very few similarities due to the different nature of this game

    Instance Attributes:
        - next_player:
        - empty_spots:
        - move_history:
    """
    next_player: str
    empty_spots: list[Optional[str]]
    move_history: list[Optional[str]]

    # Private Instance Attributes:
    #   - _board: a nested list representing a tictactoe board
    #   - _board_side: the side length of the board
    _board: list[list[str]]
    _board_side: int

    def __init__(
        self,
        board: list[list[str]],
        next_player: str = 'p1',
        move_hist: list[Optional[str]] = []
    ) -> None:
        self._board = board
        self._board_side = len(self._board)  # calculate the side length of the game board
        self.move_history = move_hist
        self.next_player = next_player
        self.empty_spots = self._find_empty_spots()

    def _find_empty_spots(self) -> list[Optional[str]]:
        empty_spots = []
        for row_idx in range(self._board_side):
            for col_idx in range(self._board_side):
                if self._board[row_idx][col_idx] == '':
                    empty_spots.append(str(row_idx) + str(col_idx))
        return empty_spots

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

        if spot in self.empty_spots:  # check if the spot is empty
            self._board[row][col] = piece
            self.empty_spots.remove(spot)
            self.next_player = 'p2' if self.next_player == 'p1' else 'p1'
            self.move_history.append(spot)
        else:
            raise ValueError(f"[!] Given spot {spot} is not empty.")

    def get_winning_piece(self) -> str:
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

        # if there are no empty spots in the board then it's a tie
        # [*] this can be improved by predicting early ties, but I won't implement it
        # right now
        if not self.empty_spots:
            return "tie"

        # otherwise there's no winner yet
        return None


# g = GameState(empty_board(3))
# print(g.empty_spots)
# g.place_piece('x', '22')
# print(g._board)
# g.get_winning_piece()


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

    def return_move(self, game: GameState, prev_move: str):
        """
        return a move in the given game state

        `prev_move` is the opponent player's most recent move, or `None` if no moves
        have been made
        """
        raise NotImplementedError


class AIRandomPlayer(Player):
    """
    An 'AI' player that simply makes random moves that are available in the game state.
    """

    def return_move(self, game: GameState, prev_move: str) -> tuple[str, str]:
        """
        return the game piece {'x', 'o'} and a move in the given game state

        `prev_move` is the opponent player's most recent move, or `None` if no moves
        have been made; not used by `AIRandomPlayer`
        """
        return self._piece, random.choice(game.empty_spots)


class AIMinimaxPlayer(Player):
    """
    An 'AI' player that employs a MiniMax algorithm on a game tree to make moves in the
    game state.

    Instance Attributes:
        -
    """
    difficulty: str

    def __init__(self, piece, difficulty) -> None:
        super().__init__()


# gt = GameState([['x', 'o', 'o'], ['o', '', 'o'], ['x', 'o', 'o']])
# print(gt._board)
# print(gt.empty_spots)
# gt.get_winning_piece()
# air = AIRandomPlayer('x')
# pc, sp = air.return_move(gt, None)
# gt.place_piece(pc, sp)


def role_to_player(role: str, piece: str) -> Player:
    """
    helper function to convert the string representation of a player's role and return a
    `Player` object accordingly; set the `Player` object's piece attribute as given
    """
    if role == "ai_random":
        return AIRandomPlayer(piece)
    elif role[:2] == "ai":
        return AIMinimaxPlayer(piece, role[-4:])
    else:
        return "human"


def piece_not(piece: str) -> str:
    """
    helper function to return the other game piece that is not the current game piece

    Preconditions:
        - piece in {'x', 'o'}

    >>> piece_not('x')
    'o'
    >>> piece_not('o')
    'x'
    """
    return 'x' if piece == 'o' else 'o'


def init_game(
    board_side: int,
    p1_piece: str,
    start_first: str,
    p2_role: str,
    p1_role: str = 'human'
) -> tuple[GameState, Player, Player]:
    """
    initialize a Tic Tac Toe game on a board of given side length `board_side`;
    return the winner of the game as well as the list of moves made in the game
    """
    assert start_first in {'p1', 'p2', 'nd'}

    # create a new game with the board's side lengtn given by `board_side`
    game = GameState(empty_board(board_side))

    # set player 2's game piece
    p2_piece = piece_not(p1_piece)

    # initialize players' classes
    p1 = role_to_player(p1_role, p1_piece)
    p2 = role_to_player(p2_role, p2_piece)

    # determine which player starts first if left up to random
    start_first = random.choice(['p1', 'p2']) if start_first == 'nd' else start_first
    # set the next player in the game state to be the first player
    game.next_player = start_first

    return game, p1, p2


if __name__ == '__main__':
    import doctest
    doctest.testmod()
