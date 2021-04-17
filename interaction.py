"""
Manipulates the DOM inside the browser and handles user interaction.

This module cannot be run with a regular CPython interpreter, because it uses
the `browser` module provided by the Btython distribution.
This module will be loaded by `index.html` and executed by the Brython
interpreter `brython.js`.
`brython_stdlib.js` provides the Python standard library for the Brython
interpreter, and allows for imports of other modules to work.
Learn more about Brython: https://brython.info

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
from browser import document as dom
from browser import html, DOMEvent, window
import tictactoe as ttt


class ThemeColor:
    """
    selection of colors used in the UI design
    """
    sel: str = "#22263f"
    unsel: str = "#7399c6"
    blue: str = "#4c94df"
    green: str = "#1ea382"
    orange: str = "#f4a83e"
    purple: str = "#6145b2"
    disabled: str = "#b0b0b0"


# GLOBAL VARIABLES
class Config:
    """
    global configurations to keep track of

    Class Attributes:
        -
    """
    BOARD_SIDE_LENGTH: int = 3
    WINNING_STEP_LEN: int = 3  # currently unused but can be used when extended
    PLAYER_1_PIECE: str = 'x'
    START_FIRST: str = "p1"  # p1 -> player 1; p2 -> player 2; nd -> not determined
    PLAYER_2_ROLE: str = "ai_random"
    PLAYER_1_COLOR: str = ThemeColor.purple
    PLAYER_2_COLOR: str = ThemeColor.green
    GAME_OBJS: dict = {}


def draw_board(table: html.TABLE, side: int) -> None:
    """
    draw the game board of a given side-length onto te given `html.TABLE`
    """
    table.text = ""
    for i in range(side):
        tr = html.TR()
        for j in range(side):
            td = html.TD(html.SPAN(Class="cell", name=f"{i}{j}"))
            tr.append(td)
        table.attach(tr)

    # set table cell size according to side length
    dom["table_adjustments"].text = f"""
    /* set table cell size for side length of {side} */
    table td{{width: {90/side}%;}}  /* (90/{side})% */
    @media screen and (min-width: 1024px)
    {{
        table td{{width: {60/side}%;}}  /* (60/{side})% */
    }}
    @media screen and (min-width: 1500px)
    {{
        table td{{width: {45/side}%;}}  /* (45/{side})% */
    }}
    """

    # update the global side length winning step length
    # global BOARD_SIDE_LENGTH
    # global WINNING_STEP_LEN
    Config.BOARD_SIDE_LENGTH = side
    Config.WINNING_STEP_LEN = side


def switch_selection(
    selected: html.BUTTON,
    button_class: str,
    colortype: str = "background-color"
) -> None:
    """
    helper function to remove darkened background from all buttons in the
    `button_class`, and darken the `selected` button
    changes the foreground or background collor based on the `colortype` option
    """

    # clear background color for all buttons in the `button_class`
    for b in dom.select(button_class):
        if b.name != selected.name:
            b.attrs["style"] = ""

    # darken `selected` button's background color
    selected.attrs["style"] = f"{colortype}: {ThemeColor.sel};"


def disable_button(button: html.BUTTON) -> None:
    """
    helper function to disable a specific button and set its style to show the
    disabled state
    """
    button.attrs["style"] = ""
    button.classList.add("btn-dis")
    button.disabled = True


def enable_button(button: html.BUTTON) -> None:
    """
    helper function to disable a specific button and set its style to show the
    disabled state
    """
    button.classList.remove("btn-dis")
    button.disabled = False


def ev_board_size(event: DOMEvent) -> None:
    """
    change the board size based on the given button event
    """
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-len")

    # grab new side length and redraw board
    new_side_len = int(target.name[-1])
    draw_board(dom['board'], new_side_len)

    # disable or enable winning step buttons as necessary
    for b in dom.select('.btn-win'):
        if int(b.name[-1]) > new_side_len:
            disable_button(b)
        elif int(b.name[-1]) == new_side_len:
            enable_button(b)
            b.attrs["style"] = f"background-color: {ThemeColor.sel};"
        else:
            enable_button(b)
            b.attrs["style"] = f"background-color: {ThemeColor.unsel};"

    # bind cell functions for each cell
    bind_cells()

    # log the change in the broswer console
    print(f"Changed board side length to: {new_side_len}")


def ev_win_step(event: DOMEvent) -> None:
    """
    [!] this function is currently unused, but may be used in the future
    change the number of steps required to win the game based on the
    given button event
    write the result into the configuration variable `Config.WINNING_STEP_LEN`
    """
    # global WINNING_STEP_LEN
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-win")

    # grab new winning length and set the global variable
    Config.WINNING_STEP_LEN = int(target.name[-1])

    # log the change in the broswer console
    print(f"Set winning step length to: {Config.WINNING_STEP_LEN}")


def ev_player1_piece(event: DOMEvent) -> None:
    """
    change the game piece (x/o) used by player 1 based on the given
    button event
    write the result into the configuration variable `Config.PLAYER_1_PIECE`
    """
    # global PLAYER_1_PIECE
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-piece", colortype="color")

    # grab new player 1 game piece and set the global variable
    Config.PLAYER_1_PIECE = target.name[-1]

    # log the change in the broswer console
    print(f"Changed Player 1's game piece to: {Config.PLAYER_1_PIECE}")


def ev_who_starts_first(event: DOMEvent) -> None:
    """
    change the whether player 1 or player 2 starts first, or determine
    by a random draw, based on the given button event
    write the result into the configuration variable `Config.START_FIRST`
    """
    # global START_FIRST
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-st")

    # grab new starting player and set the global variable
    Config.START_FIRST = target.name[-2:]

    # log the change in the broswer console
    print(f"Player {Config.START_FIRST} will start first.")


def ev_player_2_role(event: DOMEvent) -> None:
    """
    change the role of player 2, between `another_human`, `ai_random`, `ai_easy`,
    and `ai_hard`
    write the result into the configuration variable `Config.PLAYER_2_ROLE`
    also adjust `Config.PLAYER_2_COLOR` to be green if player 2 is an AI, or orange if
    player 2 is a human
    """
    # global PLAYER_2_ROLE
    # global PLAYER_2_COLOR
    target = event.target

    # find the selected option
    selected = [option.value for option in target if option.selected]

    # grab new starting player and set the global variable
    Config.PLAYER_2_ROLE = selected[0]

    # change game piece color depending on player 2's role
    if Config.PLAYER_2_ROLE[:2] == "ai":
        Config.PLAYER_2_COLOR = ThemeColor.green
    else:
        Config.PLAYER_2_COLOR = ThemeColor.orange

    # log the change in the broswer console
    print(f"Player 2 will be {Config.PLAYER_2_ROLE}")


def bind_cells() -> None:
    """
    """
    for c in dom.select('.cell'):
        c.bind("mouseover", cell_hover)
        c.bind("mouseout", cell_unhover)
        c.bind("click", cell_click)


def cell_hover(event: DOMEvent) -> None:
    """
    """
    target = event.target
    # print(f"hover {target.attrs['name']}")
    which_player = Config.GAME_OBJS["game"].next_player
    piece = Config.PLAYER_1_PIECE if which_player == "p1" else ttt.piece_not(Config.PLAYER_1_PIECE)
    target.text = piece


def cell_unhover(event: DOMEvent) -> None:
    """
    """
    target = event.target
    # print(f"hover {target.attrs['name']}")
    target.text = ''


def cell_click(event: DOMEvent) -> None:
    """
    """
    target = event.target
    # print(f"click {target.attrs['name']}")
    which_player = Config.GAME_OBJS["game"].next_player
    piece = Config.PLAYER_1_PIECE if which_player == "p1" else ttt.piece_not(Config.PLAYER_1_PIECE)
    target.text = piece
    target.unbind("click", cell_click)
    target.unbind("mouseout", cell_unhover)
    target.unbind("mouseover", cell_hover)
    if which_player == 'p1':
        target.attrs["style"] = f"color: {Config.PLAYER_1_COLOR};"
    else:
        target.attrs["style"] = f"color: {Config.PLAYER_2_COLOR};"
    ev_game_round(event)


def draw_piece(piece: str, spot: str):
    """
    helper function to draw a given game piece at the given spot on the game board UI
    """
    for c in dom.select('.cell'):
        if c.attrs["name"] == spot:
            c.text = piece
            c.unbind("click", cell_click)
            c.unbind("mouseout", cell_unhover)
            c.unbind("mouseover", cell_hover)
            if piece == Config.PLAYER_1_PIECE:
                c.attrs["style"] = f"color: {Config.PLAYER_1_COLOR};"
            else:
                c.attrs["style"] = f"color: {Config.PLAYER_2_COLOR};"


def check_winner(game: ttt.GameState) -> bool:
    """
    given the game state, check for winners;
    if a winner is found, announce it to the game status and return `True`;
    otherwise prompt the next player to play, and return `False`
    """
    # check for winners
    if winning_piece := game.get_winning_piece():
        # find out whether player 1 or 2 won the game
        winner_num = 1 if winning_piece == Config.PLAYER_1_PIECE else 2

        # announce the winner
        dom['game_status'].html = f"""
            <span style="color: #dd426e; display: inline;">
                Player {winner_num} wins!
            </span><br>
            <span style="font-size: 0.7em; display: inline;">
                Press the Reset button to start a new game.
            </span>
        """
        # dom['game_status'].attrs["style"] = ""

        # disable game board cells
        for c in dom.select('.cell'):
            c.unbind("click", cell_click)
            c.unbind("mouseout", cell_unhover)
            c.unbind("mouseover", cell_hover)

        # log the winner in the browser console
        print(f"Winner is Player {winner_num}!")

        return True

    # if no winners, announce the next player's turn
    else:
        dom['game_status'].html = f"""
            Player {game.next_player[-1]}'s turn.
        """

        return False


def ev_game_round(event: DOMEvent) -> None:
    """
    advance a round of the game based on the current game state
    can be triggered by the start_game function or a player making a move
    """
    target = event.target
    game = Config.GAME_OBJS["game"]
    player = Config.GAME_OBJS[game.next_player]

    print(player)

    # when we start a fresh game
    if target.attrs['name'] == "start" and player != "human":
        piece, spot = player.return_move(game, None)
        game.place_piece(piece, spot)
        draw_piece(piece, spot)

    # when getting called by a human player, place the piece for the human
    elif "cell" in target.classList:
        spot = target.attrs['name']
        if game.next_player == "p1":
            piece = Config.PLAYER_1_PIECE
        else:
            piece = ttt.piece_not(Config.PLAYER_1_PIECE)
        game.place_piece(piece, spot)

    # check for winners; exit the function if a winner is found
    if check_winner(game):
        return

    # make the next move if the next player is not human
    player_next = Config.GAME_OBJS[game.next_player]
    if player_next != "human":
        piece, spot = player_next.return_move(game, game.move_history[-1])
        game.place_piece(piece, spot)
        draw_piece(piece, spot)

    # check for winners again
    check_winner(game)


def ev_start_game(event: DOMEvent) -> None:
    """
    start the game by calling the initializer and calling the first round
    """
    # global GAME_OBJS
    game, p1, p2 = ttt.init_game(
        Config.BOARD_SIDE_LENGTH,
        Config.PLAYER_1_PIECE,
        Config.START_FIRST,
        Config.PLAYER_2_ROLE,
        p1_role="human"
    )

    # update the game objects store according to the newly initialized game
    Config.GAME_OBJS["game"] = game
    Config.GAME_OBJS["p1"] = p1
    Config.GAME_OBJS["p2"] = p2

    # bind trigger functions for each cell of the game board UI
    bind_cells()

    # replace the start button with the reset button
    event.target.attrs["style"] = "display: none;"
    dom["btn_reset"].attrs["style"] = ""

    ev_game_round(event)


def ev_reset_game(event) -> None:
    """
    this function gets triggered by the reset button, and it refershes the browser page
    """
    window.location.reload()


if __name__ == '__main__':
    print("https://sammdu.com")

    # draw a 3x3 board by default
    draw_board(dom['board'], 3)

    # indicate that the game is ready
    dom['game_status'].html = """
    Please select your options,
    <span style="display: inline-block;">and start the game below!</span>
    """

    # enforce a deafult value for the player 2 role select menu
    dom["player_2_role"].value = Config.PLAYER_2_ROLE

    # bind functions to buttons
    for b in dom.select('.btn-len'):
        b.bind("click", ev_board_size)
    # for b in dom.select('.btn-win'):
    #     b.bind("click", ev_win_step)
    for b in dom.select('.btn-piece'):
        b.bind("click", ev_player1_piece)
    for b in dom.select('.btn-st'):
        b.bind("click", ev_who_starts_first)
    dom["player_2_role"].bind("change", ev_player_2_role)
    dom["btn_start"].bind("click", ev_start_game)
    dom["btn_reset"].bind("click", ev_reset_game)
