"""
This program replicates the classic Breakout game.
Also known as the BrickBreaker game on blackberries.

The program takes in the difficulty level from the
user and accordingly provides a stage.
"""

import tkinter
import time
from PIL import ImageTk
from PIL import Image
import random

CANVAS_WIDTH = 540
CANVAS_HEIGHT = 600
BALL_SIZE = 20
PADDLE_WIDTH = 61
PADDLE_Y = CANVAS_HEIGHT - 40
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 30

def main():
    print("Please choose a level from 1 to 5")
    print("Level 1: Reflects at standard angle and standard speed")
    print("Level 2: Reflects at standard angle and a slightly higher speed")
    print("Level 3: Reflects at steeper angle and higher speed")
    print("Level 4: Reflects at a random angle every time and standard speed")
    print("Level 5: There are obstacles in the way of all the bricks")
    lev = int(input("Please enter level number: "))
    if lev == 1:
        level_1_to_4([-3], [8], 1/50)
    elif lev == 2:
        level_1_to_4([-3], [8], 1/100)
    elif lev == 3:
        level_1_to_4([-5], [12], 1/80)
    elif lev == 4:
        level_1_to_4([-1, -15, -8], [8], 1/50)
    elif lev == 5:
        level_5([-3], [12], 1/60)


def level_5(dx, dy, pause):
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'bounce')
    ball = canvas.create_oval(0, 200, BALL_SIZE, BALL_SIZE + 200, fill='black')
    img3 = ImageTk.PhotoImage(Image.open("Images/paddle.png"))
    paddle = canvas.create_image(0, PADDLE_Y, anchor="nw", image=img3)
    score = 0
    blockline1 = []
    blockline2 = []
    blockline3 = []
    blocks = [blockline1, blockline2, blockline3]
    img = ImageTk.PhotoImage(Image.open("Images/bricks.png"))
    for i in range(3):
        for j in range(CANVAS_WIDTH // BLOCK_WIDTH):
            blocks[i].append(canvas.create_image(j * BLOCK_WIDTH, i * BLOCK_HEIGHT * 2, anchor="nw", image=img))

    img2 = ImageTk.PhotoImage(Image.open("Images/Stone.png"))
    stone1 = canvas.create_image(0, BLOCK_HEIGHT, anchor="nw", image=img2)
    stone2 = canvas.create_image(0, BLOCK_HEIGHT * 3, anchor="nw", image=img2)
    stone3 = canvas.create_image(0, BLOCK_HEIGHT * 5, anchor="nw", image=img2)
    update_stone1 = 8
    update_stone2 = 6
    update_stone3 = 4

    display = canvas.create_text(CANVAS_WIDTH - 140, 20, anchor='w', font='Courier 20', text='Score = ' + (str(score)))

    update_y = dy[random.randint(0, len(dy)-1)]
    update_x = dx[random.randint(0, len(dx)-1)]

    while not (at_bottom_border(canvas, ball)) and not (empty(canvas)):
        mouse_x = canvas.winfo_pointerx()
        if mouse_x <= (CANVAS_WIDTH - PADDLE_WIDTH) and mouse_x >= 0:
            canvas.moveto(paddle, mouse_x, PADDLE_Y)

        if get_left_x(canvas, stone1) > (CANVAS_WIDTH - BLOCK_WIDTH) or get_left_x(canvas, stone1) < 0:
            update_stone1 = -update_stone1
        if get_left_x(canvas, stone2) > (CANVAS_WIDTH - BLOCK_WIDTH) or get_left_x(canvas, stone2) < 0:
            update_stone2 = -update_stone2
        if get_left_x(canvas, stone3) > (CANVAS_WIDTH - BLOCK_WIDTH) or get_left_x(canvas, stone3) < 0:
            update_stone3 = -update_stone3

        if at_top_border(canvas, ball):
            for i in range(len(dy)):
                dy[i] = -dy[i]
            update_y = dy[random.randint(0, len(dy)-1)]
            canvas.moveto(ball, get_left_x(canvas, ball), get_top_y(canvas, ball) + 2)

        if hit_paddle(canvas, ball, paddle):
            for i in range(len(dy)):
                dy[i] = -dy[i]
            update_y = dy[random.randint(0, len(dy)-1)]
            update_x = dx[random.randint(0, len(dx) - 1)]
            canvas.moveto(ball, get_left_x(canvas, ball), get_top_y(canvas, ball) - 2)

        if hit_block(canvas, ball) and not (hit_paddle(canvas, ball, paddle)):
            canvas.delete(display)
            for i in range(len(dy)):
                dy[i] = -dy[i]
            update_y = dy[random.randint(0, len(dy)-1)]
            score += delete_block5(canvas, ball, display, stone1, stone2, stone3)
            display = canvas.create_text(CANVAS_WIDTH - 140, 20, anchor='w', font='Courier 20',
                                         text='Score = ' + (str(score)))
            update_x = dx[random.randint(0, len(dx) - 1)]

        if at_left_border(canvas, ball):
            for i in range(len(dx)):
                dx[i] = -dx[i]
            update_x = -update_x
            canvas.moveto(ball, get_left_x(canvas, ball) + 2, get_top_y(canvas, ball))

        if at_right_border(canvas, ball):
            for i in range(len(dx)):
                dx[i] = -dx[i]
            update_x = -update_x
            canvas.moveto(ball, get_left_x(canvas, ball) - 2, get_top_y(canvas, ball))

        # update
        canvas.move(stone1, update_stone1, 0)
        canvas.move(stone2, update_stone2, 0)
        canvas.move(stone3, update_stone3, 0)
        canvas.move(ball, update_x, update_y)
        canvas.update()

        # pause
        time.sleep(pause)

    canvas.create_text(125, 250, anchor='w', font='Courier 51', text='GAME OVER!')
    canvas.delete(display)
    canvas.create_text(200, 300, anchor='w', font='Courier 30',
                                 text='Score = ' + (str(score)))
    canvas.delete(paddle)
    canvas.delete(ball)

    canvas.mainloop()



def level_1_to_4(dx, dy, pause):
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'bounce')
    ball = canvas.create_oval(0, 100, BALL_SIZE, BALL_SIZE + 100, fill='black')
    img1 = ImageTk.PhotoImage(Image.open("Images/paddle.png"))
    paddle = canvas.create_image(0, PADDLE_Y, anchor="nw", image=img1)
    score = 0
    blockline1 = []
    blockline2 = []
    blockline3 = []
    blocks = [blockline1, blockline2, blockline3]
    img = ImageTk.PhotoImage(Image.open("Images/bricks.png"))
    for i in range(3):
        for j in range(CANVAS_WIDTH // BLOCK_WIDTH):
            blocks[i].append(canvas.create_image(j * BLOCK_WIDTH, i * BLOCK_HEIGHT, anchor="nw", image=img))

    display = canvas.create_text(CANVAS_WIDTH - 140, 20, anchor='w', font='Courier 20', text='Score = ' + (str(score)))

    update_y = dy[random.randint(0, len(dy)-1)]
    update_x = dx[random.randint(0, len(dx)-1)]

    while not (at_bottom_border(canvas, ball)) and not (empty(canvas)):
        mouse_x = canvas.winfo_pointerx()
        if mouse_x <= (CANVAS_WIDTH - PADDLE_WIDTH) and mouse_x >= 0:
            canvas.moveto(paddle, mouse_x, PADDLE_Y)

        if at_top_border(canvas, ball):
            for i in range(len(dy)):
                dy[i] = -dy[i]
            update_y = dy[random.randint(0, len(dy)-1)]
            canvas.moveto(ball, get_left_x(canvas, ball), get_top_y(canvas, ball) + 2)

        if hit_paddle(canvas, ball, paddle):
            for i in range(len(dy)):
                dy[i] = -dy[i]
            update_y = dy[random.randint(0, len(dy)-1)]
            update_x = dx[random.randint(0, len(dx) - 1)]
            canvas.moveto(ball, get_left_x(canvas, ball), get_top_y(canvas, ball) - 2)

        if hit_block(canvas, ball) and not (hit_paddle(canvas, ball, paddle)):
            canvas.delete(display)
            for i in range(len(dy)):
                dy[i] = -dy[i]
            update_y = dy[random.randint(0, len(dy)-1)]
            score += delete_block(canvas, ball, display)
            display = canvas.create_text(CANVAS_WIDTH - 140, 20, anchor='w', font='Courier 20',
                                         text='Score = ' + (str(score)))
            update_x = dx[random.randint(0, len(dx) - 1)]

        if at_left_border(canvas, ball):
            for i in range(len(dx)):
                dx[i] = -dx[i]
            update_x = -update_x
            canvas.moveto(ball, get_left_x(canvas, ball) + 2, get_top_y(canvas, ball))

        if at_right_border(canvas, ball):
            for i in range(len(dx)):
                dx[i] = -dx[i]
            update_x = -update_x
            canvas.moveto(ball, get_left_x(canvas, ball) - 2, get_top_y(canvas, ball))

        # update
        canvas.move(ball, update_x, update_y)
        canvas.update()

        # pause
        time.sleep(pause)

    canvas.create_text(125, 250, anchor='w', font='Courier 51', text='GAME OVER!')
    canvas.delete(display)
    canvas.create_text(200, 300, anchor='w', font='Courier 30',
                                 text='Score = ' + (str(score)))
    canvas.delete(paddle)
    canvas.delete(ball)

    canvas.mainloop()


def at_top_border(canvas, ball):
    curr_y = get_top_y(canvas, ball)
    return curr_y <= 0

def at_bottom_border(canvas, ball):
    curr_y = get_top_y(canvas, ball)
    return curr_y >= (CANVAS_HEIGHT - BALL_SIZE)


def at_right_border(canvas, ball):
    curr_x = get_left_x(canvas, ball)
    return curr_x >= (CANVAS_WIDTH - BALL_SIZE)

def at_left_border(canvas, ball):
    curr_x = get_left_x(canvas, ball)
    return curr_x <= 0

def hit_paddle(canvas, ball, paddle):
    ball_coords = canvas.coords(ball)
    x1 = ball_coords[0]
    y1 = ball_coords[1]
    x2 = ball_coords[2]
    y2 = ball_coords[3]
    overlap = canvas.find_overlapping(x1, y1, x2, y2)
    for i in range(len(overlap)):
        if overlap[i] == paddle:
            return True
    return False

def hit_block(canvas, ball):
    ball_coords = canvas.coords(ball)
    x1 = ball_coords[0]
    y1 = ball_coords[1]
    x2 = ball_coords[2]
    y2 = ball_coords[3]
    overlap = canvas.find_overlapping(x1, y1, x2, y2)
    return len(overlap) > 1

def on_screen(canvas, ball):
    curr_y = get_top_y(canvas, ball)
    return curr_y <= CANVAS_HEIGHT

def delete_block(canvas, ball, display):
    ball_coords = canvas.coords(ball)
    overlap = canvas.find_overlapping(ball_coords[0], ball_coords[1], ball_coords[2], ball_coords[3])
    count = 0
    for i in range(len(overlap)):
        if overlap[i] != ball and overlap[i] != display:
            canvas.delete(overlap[i])
            count += 1
    return count

def delete_block5(canvas, ball, display, stone1, stone2, stone3):
    ball_coords = canvas.coords(ball)
    overlap = canvas.find_overlapping(ball_coords[0], ball_coords[1], ball_coords[2], ball_coords[3])
    count = 0
    for i in range(len(overlap)):
        if overlap[i] != ball and overlap[i] != display and overlap[i] != stone1 and overlap[i] != stone2 and overlap[i] != stone3:
            canvas.delete(overlap[i])
            count += 1
    return count

def empty(canvas):
    overlap = canvas.find_overlapping(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    return len(overlap) < 4




def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


def get_left_x(canvas, object):
    return canvas.coords(object)[0]

def get_top_y(canvas, object):
    return canvas.coords(object)[1]


if __name__ == "__main__":
    main()