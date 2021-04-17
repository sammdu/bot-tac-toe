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
        - placement:
        - is_x_move:
        - x_win_prob:
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
        Initialize a new game tree.

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
        find a particular subtree whose node is the given spot
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

    # def insert_placement_sequence(
    #     self,
    #     placements: list[str],
    #     win_score: float = 0.0
    # ) -> None:
    #     """
    #     insert a sequence of piece placements into the current tree such that the first
    #     plecement in the sequence forms a subtree in the current game tree, and the
    #     subsequent placements recursively become descendents of the first spot
    #     """
    #     return None

    # def _update_x_win_score(self) -> None:
    #     """
    #     recalculate the winning scoreability for x for the current game tree
    #
    #     assume each subtree has the correct `x_win_score`, and either:
    #         - calculate the max of subtree scoreabilities, if the current node is `x`;
    #           x acts as the maximizer of ``
    #         - calculate the min of subtree scoreabilities
    #     """
    #     return None


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['typing'],
        'allowed-io': [],
        'max-line-length': 100,
        'disable': ['E1136']
    })
