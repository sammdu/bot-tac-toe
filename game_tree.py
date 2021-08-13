"""
The TicTacToe game tree and peripheral functions.

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
from typing import Optional, Any


class GameTree:
    """
    A decision tree for Tic Tac Toe game placements.

    [c] This class is adapted from "CSC111 Winter 2021 Assignment 2: Trees, Chess, and
        Artificial Intelligence (Game Tree)", by David Liu and Isaac Waller

    Each node in the tree stores a piece placement (`placement`), whether `x` places the
    piece (`is_x_move`), and the score that is maximized when 'x' is likely to win

    Instance Attributes:
        - placement: the placement spot of the piece represented by this tree node
        - is_x_move: True if this node's plecement is done by 'x', False otherwise
        - x_win_score: the Minimax utility score that is large if 'x' is likely to win and
          small if 'o' is likely to win
    """
    placement: Optional[str]
    is_x_move: bool
    x_win_score: int

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      placement by the current player
    _subtrees: list

    def __init__(
            self,
            placement: Optional[str] = None,
            is_x_move: bool = True,
            x_win_score: int = 0
    ) -> None:
        """
        initialize a new game tree

        >>> gt = GameTree()
        >>> gt.placement is None
        True
        >>> gt.is_x_move
        True
        >>> gt.x_win_score
        0
        """
        self.placement = placement
        self.is_x_move = is_x_move
        self._subtrees = []
        self.x_win_score = x_win_score

    def get_subtrees(self) -> list:
        """
        return all subtrees under the current game tree
        """
        return self._subtrees

    def find_subtree_by_spot(self, spot: str) -> Any:
        """
        find a particular subtree whose node contains the given spot

        this is only a depth-1 enumeration of the subtrees of the given node, and not an
        exhausive search in the entire game tree
        """
        for subtree in self._subtrees:
            if subtree.placement == spot:
                return subtree
        return None

    def add_subtree(self, subtree: Any) -> None:
        """
        append the given subtree to the current game tree's list of subtrees
        """
        self._subtrees.append(subtree)

    def __str__(self, depth: int = 0) -> str:
        """
        return a string representation of the current game tree
        """
        piece = 'x' if self.is_x_move else 'o'
        string = ('    ' * depth) + "  `---" + \
            f"[{piece} -> ({self.placement})]:" + \
            f" {self.x_win_score} \n"
        if self._subtrees == []:
            return string
        else:
            for subtree in self._subtrees:
                string += subtree.__str__(depth + 1)
            return string


if __name__ == '__main__':
    import doctest
    doctest.testmod()
