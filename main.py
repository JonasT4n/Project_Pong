from GameAttribute import *

pg.init()

# 2 Player Game Play
def on_game_2p_mode():
    # Clean Up the Group
    listSpriteGame.empty()
    global timePlay, defaultTimePlay

    # Creating Objects onto the Screen
    pad_1 = Paddle(RED, 8, 80)
    pad_1.setPosition(30, 200)
    pad_2 = Paddle(BLUE, 8, 80)
    pad_2.setPosition(682, 200)
    ball = Ball(LIGHTBLUE, 10)
    ball.setSpeed(10, 10)

    # Adding Object into Group
    listSpriteGame.add(pad_1, pad_2)
    listSpriteGame.add(ball)

    # Run and Event
    is_run: bool = True
    while is_run:
        clock.tick(fps)
        screen.screen.fill(WHITE)

        # Player and Control
        pad_1.control_side(pg.K_w, pg.K_s)
        pad_2.control_side(pg.K_UP, pg.K_DOWN)
        ball.movement2p()
        ball.paddle_isMove(pad_1, pad_2)

        # Object Collide
        if ball.isCollideWith(pad_1):
            ball.bounce_sides()
        if ball.isCollideWith(pad_2):
            ball.bounce_sides()

        # Scoring System
        score_p1 = pg.font.Font(fontStyle, 30).render(str(pad_1.score), False, BLACK)
        score_p2 = pg.font.Font(fontStyle, 30).render(str(pad_2.score), False, BLACK)
        screen.screen.blit(score_p1, [40, 20])
        screen.screen.blit(score_p2, [665, 20])
        if ball.getPositionX() <= 0:
            pad_2.score += 1
        if ball.getPositionX() + ball.getSize()[0] >= win_size[0]:
            pad_1.score += 1

        # Time Table
        timePlay -= 1 / fps
        display_time(screen.screen, timePlay, fontStyle)
        if timePlay <= 0:
            direction["GameOver"] = True
            is_run = False

        listSpriteGame.update()
        listSpriteGame.draw(screen.screen)

        printText(screen.screen, "<Press ESC to Pause>", 12, fontStyle, [600, 465], color=BLACK)

        # Events
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

# 4 Player Game Play
def on_game_4p_mode():
    # Clean Up the Group
    listSpriteGame.empty()
    global timePlay, defaultTimePlay

    # Creating Objects
    pad_1 = Paddle(RED, 8, 80)
    pad_1.setPosition(30, 200)
    pad_2 = Paddle(YELLOW, 150, 8)
    pad_2.setPosition(middle_placement[0] - (pad_2.getSize()[0] // 2), 30)
    pad_3 = Paddle(GREEN, 150, 8)
    pad_3.setPosition(middle_placement[0] - (pad_3.getSize()[0] // 2), 450 - pad_3.getSize()[1])
    pad_4 = Paddle(BLUE, 8, 80)
    pad_4.setPosition(682, 200)
    ball = Ball(LIGHTBLUE, 10)
    ball.setSpeed(8, 8)

    # Adding Object into the Group
    listSpriteGame.add(pad_1, pad_2, pad_3, pad_4, ball)

    # Update and Events
    is_run = True
    while is_run:

        clock.tick(fps)
        screen.screen.fill(WHITE)

        # PLayer and Control
        pad_1.control_side(pg.K_w, pg.K_s)
        pad_2.control_floor(pg.K_f, pg.K_g)
        pad_3.control_floor(pg.K_k, pg.K_l)
        pad_4.control_side(pg.K_UP, pg.K_DOWN)
        ball.movement4p()
        ball.paddle_isMove(pad_1, pad_2, pad_3, pad_4)

        # Object Collide
        if ball.isCollideWith(pad_1):
            ball.bounce_sides()
        if ball.isCollideWith(pad_2):
            ball.bounce_upsidedown()
        if ball.isCollideWith(pad_3):
            ball.bounce_upsidedown()
        if ball.isCollideWith(pad_4):
            ball.bounce_sides()

        # Scoring System
        score_p1 = pg.font.Font(fontStyle, 30).render(str(pad_1.score), False, BLACK)
        score_p2 = pg.font.Font(fontStyle, 30).render(str(pad_2.score), False, BLACK)
        score_p3 = pg.font.Font(fontStyle, 30).render(str(pad_3.score), False, BLACK)
        score_p4 = pg.font.Font(fontStyle, 30).render(str(pad_4.score), False, BLACK)
        screen.screen.blit(score_p1, [40, 20])
        screen.screen.blit(score_p2, [665, 20])
        screen.screen.blit(score_p3, [40, 430])
        screen.screen.blit(score_p4, [665, 430])
        if ball.getPositionX() <= 0:
            pad_2.score += 1
            pad_3.score += 1
            pad_4.score += 1
        if ball.getPositionX() + ball.getSize()[0] >= win_size[0]:
            pad_1.score += 1
            pad_2.score += 1
            pad_3.score += 1
        if ball.getPositionY() <= 0:
            pad_1.score += 1
            pad_3.score += 1
            pad_4.score += 1
        if ball.getPositionY() + ball.getSize()[1] >= win_size[1]:
            pad_1.score += 1
            pad_2.score += 1
            pad_4.score += 1

        # Time Table
        timePlay -= 1 / fps
        display_time(screen.screen, timePlay, fontStyle)
        if timePlay <= 0:
            direction["GameOver"] = True
            is_run = False

        printText(screen.screen, "<Press ESC to Pause>", 12, fontStyle, [600, 465], color=BLACK)

        listSpriteGame.update()
        listSpriteGame.draw(screen.screen)

        # Events
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

# Game Over Menu
def on_gameOver():
    # Clean up the Group Sprites
    listSpriteMenu.empty()
    screen.setBackGroundImage("images\\backPause.png")

    # Adding Objects
    global timePlay, defaultTimePlay
    timePlay = defaultTimePlay
    txt_timesUp = pg.font.Font(fontStyle, 40).render("Time Over!!", False, RED)
    btn_playAgain = CustomButton([180, 50], btn_image1, "Restart")
    btn_playAgain.setFont(fontStyle, 30)
    btn_playAgain.setPosition(middle_placement[0] - (btn_playAgain.getSize()[0] // 2), 240)

    btn_quitMenu = CustomButton([180, 50], btn_image1, "Menu")
    btn_quitMenu.setFont(fontStyle, 30)
    btn_quitMenu.setPosition(middle_placement[0] - (btn_quitMenu.getSize()[0] // 2), 300)

    # Adding Object into Group
    listSpriteMenu.add(btn_playAgain, btn_quitMenu)

    # Events and Update
    is_run = True
    while is_run:

        clock.tick(60)
        screen.screen.blit(txt_timesUp, [middle_placement[0] - (40 * 2) - (len("Time Over!!") * 2) - 5, 120])

        on_mouse_button["PlayAgain"] = btn_playAgain.onMouseMotionChange(btn_image2)
        on_mouse_button["QuitGame"] = btn_quitMenu.onMouseMotionChange(btn_image2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                is_run = False

            if event.type == pg.MOUSEBUTTONUP:
                if on_mouse_button["PlayAgain"] is True:
                    direction["GameOver"] = False
                    is_run = False

                if on_mouse_button["QuitGame"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Menu"] = True
                    is_run = False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()

# Main Menu
def on_menu():
    # Empty up the Group
    listSpriteMenu.empty()
    screen.setBackGroundImage("images\\Menu.png")

    # Init Objects
    btn_play = CustomButton([180, 50], btn_image1, "Play")
    btn_play.setPosition(middle_placement[0] - (btn_play.getSize()[0] // 2), 260)
    btn_play.setFont(fontStyle, 30)

    btn_option = CustomButton([180, 50], btn_image1, "Option")
    btn_option.setPosition(middle_placement[0] - (btn_option.getSize()[0] // 2), 320)
    btn_option.setFont(fontStyle, 30)

    btn_quit = CustomButton([180, 50], btn_image1, "Quit")
    btn_quit.setPosition(middle_placement[0] - (btn_quit.getSize()[0] // 2), 380)
    btn_quit.setFont(fontStyle, 30)

    # Adding Obj into the Group
    listSpriteMenu.add(btn_play, btn_option, btn_quit)

    # Run and Event
    is_run: bool = True
    while is_run:

        clock.tick(fps)

        on_mouse_button["Play"] = btn_play.onMouseMotionChange(btn_image2)
        on_mouse_button["Option"] = btn_option.onMouseMotionChange(btn_image2)
        on_mouse_button["Quit"] = btn_quit.onMouseMotionChange(btn_image2)

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

                if on_mouse_button["Quit"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Quit"] = True
                    is_run = False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()

# Pause Game Play Menu
def on_pause(**kwargs):
    # Clean the Group and Screen
    listSpriteMenu.empty()
    screen.setBackGroundImage("images\\backPause.png")

    # Init Objects
    btn_resume = CustomButton([180, 50], btn_image1, "Resume")
    btn_resume.setPosition(middle_placement[0] - (btn_resume.getSize()[0] // 2), 240)
    btn_resume.setFont(fontStyle, 30)

    btn_quit = CustomButton([180, 50], btn_image1, "Quit")
    btn_quit.setPosition(middle_placement[0] - (btn_quit.getSize()[0] // 2), 300)
    btn_quit.setFont(fontStyle, 30)

    # Adding Object into Group
    listSpriteMenu.add(btn_resume, btn_quit)

    # Update and Events
    is_run = True
    while is_run:

        on_mouse_button["Resume"] = btn_resume.onMouseMotionChange(btn_image2)
        on_mouse_button["QuitGame"] = btn_quit.onMouseMotionChange(btn_image2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Quit App
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                return False

            if event.type == pg.KEYDOWN:
                # Back to Game Play
                if event.key == pg.K_ESCAPE:
                    return True

            if event.type == pg.MOUSEBUTTONUP:
                # Resume the Game
                if on_mouse_button["Resume"] is True:
                    return True

                # Quit the Game
                if on_mouse_button["QuitGame"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Menu"] = True
                    return False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()

# Option Menu
def on_option(mode_c):
    # Clean Up the Group
    listSpriteMenu.empty()
    screen.setBackGroundImage("images\\bground.png")

    # Init Objects
    btn_2pMode = CustomButton([180, 50], btn_image1, "2-Player")
    btn_2pMode.setFont(fontStyle, 30)
    btn_2pMode.setPosition(160 - (btn_2pMode.getSize()[0] // 2), 120)
    if mode_c["2Player"] is True:
        btn_2pMode.setDefaultImage(btn_image2)
        btn_2pMode.unclickable = True

    btn_4pMode = CustomButton([180, 50], btn_image1, "4-Player")
    btn_4pMode.setFont(fontStyle, 30)
    btn_4pMode.setPosition(160 - (btn_2pMode.getSize()[0] // 2), 180)
    if mode_c["4Player"] is True:
        btn_4pMode.setDefaultImage(btn_image2)
        btn_4pMode.unclickable = True

    btn_back = CustomButton([180, 50], btn_image1, "Back")
    btn_back.setPosition(middle_placement[0] - (btn_back.getSize()[0] // 2), 400)
    btn_back.setFont(fontStyle, 30)

    # Add Object into Group
    listSpriteMenu.add(btn_2pMode)
    listSpriteMenu.add(btn_4pMode)
    listSpriteMenu.add(btn_back)

    # Update and Event
    is_run = True
    while is_run:

        on_mouse_button["2P"] = btn_2pMode.onMouseMotionChange(btn_image2)
        on_mouse_button["4P"] = btn_4pMode.onMouseMotionChange(btn_image2)
        on_mouse_button["Back"] = btn_back.onMouseMotionChange(btn_image2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                for d in direction:
                    direction[d] = False
                direction["Quit"] = True
                is_run = False

            if event.type == pg.MOUSEBUTTONUP:
                if on_mouse_button["4P"] is True:
                    btn_4pMode.unclickable = True
                    btn_4pMode.setDefaultImage(btn_image2)
                    btn_2pMode.unclickable = False
                    btn_2pMode.setDefaultImage(btn_image1)
                    mode_c["2Player"] = False
                    mode_c["4Player"] = True

                if on_mouse_button["2P"] is True:
                    btn_2pMode.unclickable = True
                    btn_2pMode.setDefaultImage(btn_image2)
                    btn_4pMode.unclickable = False
                    btn_4pMode.setDefaultImage(btn_image1)
                    mode_c["2Player"] = True
                    mode_c["4Player"] = False

                if on_mouse_button["Back"] is True:
                    for d in direction:
                        direction[d] = False
                    direction["Menu"] = True
                    is_run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    for d in direction:
                        direction[d] = False
                    direction["Menu"] = True
                    is_run = False

        listSpriteMenu.update()
        listSpriteMenu.draw(screen.screen)

        pg.display.flip()

# Main Program
if __name__ == '__main__':
    is_running: bool = True
    while is_running:
        if direction["Play"] is True and mode["2Player"] is True:
            on_game_2p_mode()
        if direction["Play"] is True and mode["4Player"] is True:
            on_game_4p_mode()
        if direction["GameOver"] is True:
            on_gameOver()
        if direction["Menu"] is True:
            on_menu()
        if direction["Option"] is True:
            on_option(mode)
        if direction["Quit"] is True:
            is_running = False
    pg.quit()
    sys.exit()
