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


# GLOBAL VARIABLES
WINNING_STEP_LEN = 3
PLAYER_1_PIECE = 'x'

game_status_text = dom['game_status']


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


def draw_board(table: html.TABLE, side: int) -> None:
    """
    draw the game board of a given side-length onto te given `html.TABLE`
    """
    table.text = ""
    for i in range(side):
        tr = html.TR()
        for j in range(side):
            td = html.TD(html.SPAN(Class="cell"))
            tr.append(td)
        board.attach(tr)

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
        b.attrs["style"] = f"{colortype}: {ThemeColor.unsel};"

    # darken `selected` button's background color
    selected.attrs["style"] = f"{colortype}: {ThemeColor.sel};"


def ev_change_board_size(event: DOMEvent) -> None:
    """
    change the board size based on the given button event
    """
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-len")

    # grab new side length and redraw board
    new_side_len = int(target.name[-1])
    draw_board(board, new_side_len)

    # log the change in the broswer console
    print(f"Changed board side length to: {new_side_len}")


def ev_change_win_step(event: DOMEvent) -> None:
    """
    change the number of steps required to win the game based on the
    given button event
    """
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-win")

    # grab new winning length and set the global variable
    new_win_len = int(target.name[-1])
    global WINNING_STEP_LEN
    WINNING_STEP_LEN = new_win_len

    # log the change in the broswer console
    print(f"Set winning step length to: {WINNING_STEP_LEN}")


def ev_change_player1_piece(event: DOMEvent) -> None:
    """
    change the game piece (x/o) used by player 1 based on the given
    button event
    """
    target = event.target

    # change the button colors to reflect user selection
    switch_selection(target, ".btn-piece", colortype="color")

    # grab new winning length and set the global variable
    new_player1_piece = target.name[-1]
    global PLAYER_1_PIECE
    PLAYER_1_PIECE = new_player1_piece

    # log the change in the broswer console
    print(f"Changed Player 1's game piece to: {PLAYER_1_PIECE}")


if __name__ == '__main__':
    print("https://sammdu.com")

    # draw a 3x3 board by default
    draw_board(dom['board'], 3)

    # indicate that the game is ready
    game_status_text.html = """
    Please select your options,
    <span style="display: inline-block;">and start the game below!</span>
    """

    # bind functions to buttons
    for b in dom.select('.btn-len'):
        b.bind("click", ev_change_board_size)
    for b in dom.select('.btn-win'):
        b.bind("click", ev_change_win_step)
    for b in dom.select('.btn-piece'):
        b.bind("click", ev_change_player1_piece)
    for b in dom.select('.btn-st'):
        pass

    # dom.select('#game_status')[0].text = "Haha"
