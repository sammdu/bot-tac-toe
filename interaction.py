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
from browser import html, alert, console

game_status_text = dom['game_status']
board = dom['board']


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


if __name__ == '__main__':

    # draw a 3x3 board by default
    draw_board(board, 3)

    # indicate that the game is ready
    game_status_text.html = """
    Please select your options,
    <span style="display: inline-block;">and start the game below!</span>
    """

    # dom.select('#game_status')[0].text = "Haha"
