"""
Manipulates the DOM inside the browser and handles user interaction.

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
from browser import html, DOMEvent
from tictactoe import heyo


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
WINNING_STEP_LEN = 3
PLAYER_1_PIECE = 'x'
START_FIRST = "p1"  # p1 -> player 1; p2 -> player 2; nd -> not determined
PLAYER_2_ROLE = "another_human"
PLAYER_1_COLOR = ThemeColor.purple
PLAYER_2_COLOR = ThemeColor.orange


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
    change the number of steps required to win the game based on the
    given button event
    write the result into the global variable `WINNING_STEP_LEN`
    """
    global WINNING_STEP_LEN
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-win")

    # grab new winning length and set the global variable
    WINNING_STEP_LEN = int(target.name[-1])

    # log the change in the broswer console
    print(f"Set winning step length to: {WINNING_STEP_LEN}")


def ev_player1_piece(event: DOMEvent) -> None:
    """
    change the game piece (x/o) used by player 1 based on the given
    button event
    write the result into the global variable `PLAYER_1_PIECE`
    """
    global PLAYER_1_PIECE
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-piece", colortype="color")

    # grab new player 1 game piece and set the global variable
    PLAYER_1_PIECE = target.name[-1]

    # log the change in the broswer console
    print(f"Changed Player 1's game piece to: {PLAYER_1_PIECE}")


def ev_who_starts_first(event: DOMEvent) -> None:
    """
    change the whether player 1 or player 2 starts first, or determine
    by a random draw, based on the given button event
    write the result into the global variable `START_FIRST`
    """
    global START_FIRST
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-st")

    # grab new starting player and set the global variable
    START_FIRST = target.name[-2:]

    # log the change in the broswer console
    print(f"Player {START_FIRST} will start first.")


def ev_player_2_role(event: DOMEvent) -> None:
    """
    change the role of player 2, between `another_human`, `ai_random`, `ai_easy`,
    and `ai_hard`
    write the result into the global variable `PLAYER_2_ROLE`
    also adjust `PLAYER_2_COLOR` to be green if player 2 is an AI, or orange if
    player 2 is a human
    """
    global PLAYER_2_ROLE
    global PLAYER_2_COLOR
    target = event.target

    # find the selected option
    selected = [option.value for option in target if option.selected]

    # grab new starting player and set the global variable
    PLAYER_2_ROLE = selected[0]

    # change game piece color depending on player 2's role
    if PLAYER_2_ROLE[:2] == "ai":
        PLAYER_2_COLOR = ThemeColor.green
    else:
        PLAYER_2_COLOR = ThemeColor.orange

    # log the change in the broswer console
    print(f"Player 2 will be {PLAYER_2_ROLE}")


def bind_cells() -> None:
    for c in dom.select('.cell'):
        c.bind("mouseover", cell_hover)
        c.bind("mouseout", cell_unhover)
        c.bind("click", cell_click)


def cell_hover(event: DOMEvent) -> None:
    target = event.target
    # print(f"hover {target.attrs['name']}")
    target.text = PLAYER_1_PIECE


def cell_unhover(event: DOMEvent) -> None:
    target = event.target
    # print(f"hover {target.attrs['name']}")
    target.text = ''


def cell_click(event: DOMEvent) -> None:
    target = event.target
    # print(f"click {target.attrs['name']}")
    target.text = PLAYER_1_PIECE
    target.unbind("mouseout", cell_unhover)
    target.unbind("mouseover", cell_hover)
    target.attrs["style"] = f"color: {PLAYER_1_COLOR};"


if __name__ == '__main__':
    print("https://sammdu.com")
    print(heyo)

    # draw a 3x3 board by default
    draw_board(dom['board'], 3)

    # indicate that the game is ready
    dom['game_status'].html = """
    Please select your options,
    <span style="display: inline-block;">and start the game below!</span>
    """

    # enforce a deafult value for the player 2 role select menu
    dom["player_2_role"].value = PLAYER_2_ROLE

    # bind functions to buttons
    for b in dom.select('.btn-len'):
        b.bind("click", ev_board_size)
    for b in dom.select('.btn-win'):
        b.bind("click", ev_win_step)
    for b in dom.select('.btn-piece'):
        b.bind("click", ev_player1_piece)
    for b in dom.select('.btn-st'):
        b.bind("click", ev_who_starts_first)
    dom["player_2_role"].bind("change", ev_player_2_role)

    # bind trigger functions for each cell
    bind_cells()
