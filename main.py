import pygame as pg, os, random, sys
from Paddle import Paddle
from windowScreen import Screen
from Ball import Ball
from Button import Button

pg.init()

# Windows Attribute
win_size = [720, 480]
icon = "images\\Logo.jpg"
is_running: bool = True
clock = pg.time.Clock()
screen = Screen(win_size, "PONG!")
screen.setIcon(icon)
middle_placement = [(win_size[0] // 2), win_size[1] // 2]
fontStyle = "\\".join(list(os.getcwd().split("\\"))) + "\\Font\\comic.ttf"
on_mouse_button = {
    "Play": False,
    "Quit": False,
    "Resume":False,
    "Option":False,
    "2P": False,
    "4P": False,
    "Confirm":False,
    "QuitGame":False
}
mode = {"2Player":True, "4Player":False, "2PBot":False}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (150, 150, 150)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Grouping Objects
listSpriteGame = pg.sprite.Group()
listSpriteMenu = pg.sprite.Group()

def on_game_4p_mode():
    # Clean Up the Group
    listSpriteGame.empty()

    # Creating Objects
    pad_1 = Paddle(RED, 8, 80)
    pad_1.setPosition(15, 200)
    pad_2 = Paddle(YELLOW, 120, 8)
    pad_2.setPosition(middle_placement[0] - (pad_2.getSize()[0] // 2), 20)
    pad_3 = Paddle(GREEN, 120, 8)
    pad_3.setPosition(middle_placement[0] - (pad_3.getSize()[0] // 2), 460 - pad_3.getSize()[1])
    pad_4 = Paddle(BLUE, 8, 80)
    pad_4.setPosition(697, 200)
    ball = Ball(WHITE, 10)
    ball.setSpeed(12, 12)

    # Adding Object into the Group
    listSpriteGame.add(pad_1, pad_2, pad_3, pad_4, ball)

    # Update and Events
    is_run = True
    while is_run:

        clock.tick(60)
        screen.screen.fill(BLACK)

        pad_1.control_side(pg.K_a, pg.K_z)
        pad_2.control_floor(pg.K_c, pg.K_v)
        pad_3.control_floor(pg.K_m, pg.K_COMMA)
        pad_4.control_side(pg.K_UP, pg.K_DOWN)
        ball.movement4p()
        ball.paddle_isMove(pad_1, pad_2, pad_3, pad_4)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                is_run = False

        if ball.isCollideWith(pad_1):
            ball.bounce_sides()
        if ball.isCollideWith(pad_2):
            ball.bounce_upsidedown()
        if ball.isCollideWith(pad_3):
            ball.bounce_upsidedown()
        if ball.isCollideWith(pad_4):
            ball.bounce_sides()

        listSpriteGame.update()
        listSpriteGame.draw(screen.screen)

        pg.display.flip()

def on_game_2p_mode():
    # Clean Up the Group
    listSpriteGame.empty()

    # Creating Objects onto the Screen
    pad_1 = Paddle(RED, 8, 80)
    pad_1.setPosition(15, 200)
    pad_2 = Paddle(BLUE, 8, 80)
    pad_2.setPosition(697, 200)
    ball = Ball(WHITE, 10)
    ball.setSpeed(8, 8)

    # Adding Object into Group
    listSpriteGame.add(pad_1, pad_2)
    listSpriteGame.add(ball)

    # Run and Event
    is_run: bool = True
    while is_run:
        clock.tick(60)
        screen.screen.fill(BLACK)

        pad_1.control_side(pg.K_w, pg.K_s)
        pad_2.control_side(pg.K_UP, pg.K_DOWN)
        ball.movement2p()
        ball.paddle_isMove(pad_1, pad_2)

        if ball.isCollideWith(pad_1):
            ball.bounce_sides()
        if ball.isCollideWith(pad_2):
            ball.bounce_sides()

        score_p1 = pg.font.Font(fontStyle, 30).render(str(pad_1.score), False, WHITE)
        score_p2 = pg.font.Font(fontStyle, 30).render(str(pad_2.score), False, WHITE)
        screen.screen.blit(score_p1, [665, 40])
        screen.screen.blit(score_p2, [40, 40])

        if ball.getPositionX() <= 0:
            pad_1.score += 1
        if ball.getPositionX() + ball.getSize()[0] >= win_size[0]:
            pad_2.score += 1

        listSpriteGame.update()
        listSpriteGame.draw(screen.screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                is_run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    is_run = on_pause()

        pg.display.flip()

def on_menu():
    # Empty up the Group
    listSpriteMenu.empty()

    # Init Objects
    btn_play = Button([150, 30], "Play")
    btn_play.setPosition(middle_placement[0] - (btn_play.getSize()[0] // 2), 240)
    btn_play.setFontStyle(fontStyle)

    btn_option = Button([150, 30], "Option")
    btn_option.setPosition(middle_placement[0] - (btn_option.getSize()[0] // 2), 300)
    btn_option.setFontStyle(fontStyle)

    # Adding Obj into the Group
    listSpriteMenu.add(btn_play)
    listSpriteMenu.add(btn_option)

    # Run and Event
    is_run: bool = True
    while is_run:

        clock.tick(60)
        screen.screen.fill(BLACK)

        on_mouse_button["Play"] = btn_play.onMouseMotionChange(RED, WHITE)
        on_mouse_button["Option"] = btn_option.onMouseMotionChange(RED, WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                is_run = False

            if event.type == pg.MOUSEBUTTONUP:
                if on_mouse_button["Play"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Play"] = True
                    is_run = False

                if on_mouse_button["Option"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Option"] = True
                    is_run = False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()


def on_pause():
    # Clean the Group and Screen
    listSpriteMenu.empty()
    screen.screen.fill(BLACK)

    # Init Objects
    btn_resume = Button([150, 30], "Resume")
    btn_resume.setPosition(middle_placement[0] - (btn_resume.getSize()[0]//2), 200)
    btn_resume.setFontStyle(fontStyle)

    btn_quit = Button([150, 30], "Quit")
    btn_quit.setPosition(middle_placement[0] - (btn_quit.getSize()[0] // 2), 260)
    btn_quit.setFontStyle(fontStyle)

    # Adding Object into Group
    listSpriteMenu.add(btn_resume, btn_quit)

    # Update and Events
    is_run = True
    while is_run:

        on_mouse_button["Resume"] = btn_resume.onMouseMotionChange(RED, WHITE)
        on_mouse_button["QuitGame"] = btn_quit.onMouseMotionChange(RED, WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                return False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return True

            if event.type == pg.MOUSEBUTTONUP:
                if on_mouse_button["Resume"] is True:
                    return True

                if on_mouse_button["QuitGame"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Menu"] = True
                    return False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()

def on_option(mode_c):
    # Clean Up the Group
    listSpriteMenu.empty()
    screen.screen.fill(BLACK)

    # Init Objects
    btn_2pMode = Button([150, 30], "2-Player")
    btn_2pMode.setFontStyle(fontStyle)
    btn_2pMode.setPosition(160 - (btn_2pMode.getSize()[0] // 2), 100)
    if mode_c["2Player"] is True:
        btn_2pMode.setDefaultColor(GREY, BLACK)
        btn_2pMode.unclickable = True

    btn_4pMode = Button([150, 30], "4-Player")
    btn_4pMode.setFontStyle(fontStyle)
    btn_4pMode.setPosition(160 - (btn_2pMode.getSize()[0] // 2), 160)
    if mode_c["4Player"] is True:
        btn_4pMode.setDefaultColor(GREY, BLACK)
        btn_4pMode.unclickable = True

    # Add Object into Group
    listSpriteMenu.add(btn_2pMode)
    listSpriteMenu.add(btn_4pMode)

    # Update and Event
    is_run = True
    while is_run:

        on_mouse_button["2P"] = btn_2pMode.onMouseMotionChange(RED, WHITE)
        on_mouse_button["4P"] = btn_4pMode.onMouseMotionChange(RED, WHITE)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                is_run = False

            if event.type == pg.MOUSEBUTTONUP:
                if on_mouse_button["4P"] is True:
                    btn_4pMode.unclickable = True
                    btn_4pMode.setDefaultColor(GREY, BLACK)
                    btn_2pMode.unclickable = False
                    btn_2pMode.setDefaultColor(WHITE, BLACK)
                    mode_c["2Player"] = False
                    mode_c["4Player"] = True

                if on_mouse_button["2P"] is True:
                    btn_2pMode.unclickable = True
                    btn_2pMode.setDefaultColor(GREY, BLACK)
                    btn_4pMode.unclickable = False
                    btn_4pMode.setDefaultColor(WHITE, BLACK)
                    mode_c["2Player"] = True
                    mode_c["4Player"] = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    for d in direction:
                        direction[d] = False
                    direction["Menu"] = True
                    is_run = False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()

direction = {"Menu": True, "Quit": False, "Play": False, "Option":False}

if __name__ == '__main__':
    while is_running:
        if direction["Play"] is True and mode["2Player"] is True:
            on_game_2p_mode()
        if direction["Play"] is True and mode["4Player"] is True:
            on_game_4p_mode()
        if direction["Menu"] is True:
            on_menu()
        if direction["Option"] is True:
            on_option(mode)
        if direction["Quit"] is True:
            is_running = False
    pg.quit()