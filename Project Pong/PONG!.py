import pygame as pg
import os, time, random, sys

class Pong: # Game Play Scene

    is_running = True
    screen = None
    on_pause: bool = False
    next_scene: bool = False
    timer = 60.0 # Play Time and then Game Over
    font_size_timer, font_size_score = 20, 32
    fps: float or int = 60

    def __init__(self, size: tuple or list, title: str, icon = None):
        # Construct Menu
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption(title)
        self.icon = pg.image.load(icon)
        pg.display.set_icon(self.icon)
        self.screen.fill(BLACK)

        self.font_1 = pg.font.Font(font_ComicSansMS, self.font_size_timer)
        self.font_2 = pg.font.Font(font_ComicSansMS, self.font_size_score)

        middle_placement = (win_size[1] / 2) - (pedal_size[1] / 2)
        self.p1 = Pedal(self.screen, pedal_size,
                        [(self.screen.get_size()[0] / 2) - pedal_size[0] - (self.screen.get_size()[0] / 8 * 3), middle_placement] ,
                        WHITE, (pg.K_w, pg.K_s), speed=12)
        self.p2 = Pedal(self.screen, pedal_size,
                        [(self.screen.get_size()[0] / 2) - pedal_size[0] + (self.screen.get_size()[0] / 8 * 3), middle_placement] ,
                        WHITE, (pg.K_UP, pg.K_DOWN), speed=12)

        while self.is_running:

            clock.tick(self.fps)
            self.screen.fill(BLACK)

            if self.timer > 10.0:
                self.timer -= 1 / self.fps
                self.display_timer(GREEN)
            elif self.timer <= 0.0:
                self.timer = 0.0
                self.display_timer(WHITE)
            else:
                self.timer -= 1 / self.fps
                self.display_timer(RED)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MainMenu.next_scene = False
                    self.is_running = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.next_scene = True
                        self.is_running = False

            keys = pg.key.get_pressed()

            if keys[self.p1.key_control[0]]:
                self.p1.change_pos(-self.p1.speed)
            if keys[self.p1.key_control[1]]:
                self.p1.change_pos(self.p1.speed)
            if keys[self.p2.key_control[0]]:
                self.p2.change_pos(-self.p2.speed)
            if keys[self.p2.key_control[1]]:
                self.p2.change_pos(self.p2.speed)

            self.p1.show()
            self.p2.show()

            self.display_score(WHITE)

            pg.display.update()

        if self.next_scene is True:
            MainMenu(win_size, win_title, win_icon)
        else:
            pass

    def display_timer(self, color):
        time_table = self.font_1.render("{:.2f}".format(self.timer), False, color)
        self.screen.blit(time_table, ((self.screen.get_size()[0] / 2) - (self.font_size_timer * 2), 40))

    def display_score(self, color):
        score_table = self.font_2.render("{}-{}".format(self.p1.score, self.p2.score), False, color)
        self.screen.blit(score_table, ((self.screen.get_size()[0] / 2) - (self.font_size_timer * 2), 3))

    def pause_menu(self):
        pass

    def _resume(self):
        pass

    def _option(self):
        pass

    def _menu(self):
        pass

    def _quit(self):
        pass

class MainMenu: # the Main Menu of Game

    is_running = True
    sprites = pg.sprite.Group()
    screen = None
    on_button = {"Start":False, "Quit":False}
    next_scene: bool = False
    fps = 60

    def __init__(self, size: tuple or list, title: str, icon = None):
        # Construct Menu
        self.screen = pg.display.set_mode(size)
        pg.display.set_caption(title)
        self.icon = pg.image.load(icon)
        pg.display.set_icon(self.icon)
        self.screen.fill(BLACK)

        text_render = pg.font.Font(font_ComicSansMS, 120).render("PONG!", False, WHITE)
        self.screen.blit(text_render, (win_size[0]/4, win_size[1]/16))

        # Button Maker
        middle_placement = (win_size[0] / 2) - (btn_size[0] / 2)
        btn1 = Button(self.screen, BLACK, WHITE, btn_size, [middle_placement, 240], 20, font_ComicSansMS, "Start")
        btn2 = Button(self.screen, BLACK, WHITE, btn_size, [middle_placement, 300], 20, font_ComicSansMS, "Quit")

        while self.is_running:

            clock.tick(self.fps)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

                elif event.type == pg.MOUSEMOTION: # Mouse Motion to change Button Color
                    mouse_pos = pg.mouse.get_pos()
                    if middle_placement + btn_size[0] > mouse_pos[0] > middle_placement and 240 + btn_size[1] > mouse_pos[1] > 240:
                        btn1.change_color(RED, WHITE)
                        self.on_button["Start"] = True
                    else:
                        btn1.change_color(WHITE, BLACK)
                        self.on_button["Start"] = False

                    if middle_placement + btn_size[0] > mouse_pos[0] > middle_placement and 300 + btn_size[1] > mouse_pos[1] > 300:
                        btn2.change_color(RED, WHITE)
                        self.on_button["Quit"] = True
                    else:
                        btn2.change_color(WHITE, BLACK)
                        self.on_button["Quit"] = False

                elif event.type == pg.MOUSEBUTTONUP:
                    if self.on_button["Quit"] is True:
                        self.is_running = False
                    if self.on_button["Start"] is True:
                        self.next_scene = True
                        self.is_running = False

            pg.display.update()

        if self.next_scene is True:
            Pong(win_size, win_title, win_icon)
        else:
            pass

class Button: # Object Button

    size_txt: int = 0
    size_bg: tuple or list = [0, 0]
    text: str = "Text"
    font = None
    screen = None
    color_back: tuple or list = [0, 0, 0]
    color_text: tuple or list = [0, 0, 0]
    position = [0, 0]

    def __init__(self, screen, clr_txt:tuple or list, clr_bg: tuple or list, size_bg: tuple or list, pos, size_txt: int,
                 font, text: str):
        self.screen = screen
        self.size_bg = size_bg
        self.size_txt = size_txt
        self.text = text
        self.color_back = clr_bg
        self.color_text = clr_txt
        self.position = pos
        self.font = pg.font.Font(font, self.size_txt)

        self.rect = pg.Rect(self.position, self.size_bg)
        pg.draw.rect(self.screen, self.color_back, self.rect)
        self.render_txt = self.font.render(self.text, False, self.color_text)
        self.screen.blit(self.render_txt, (self.position[0] + (self.size_bg[0] / 3), self.position[1]))

    def change_color(self, background, text):
        self.color_back = background
        self.color_text = text
        self.rect = pg.Rect(self.position, self.size_bg)
        pg.draw.rect(self.screen, self.color_back, self.rect)
        self.render_txt = self.font.render(self.text, False, self.color_text)
        self.screen.blit(self.render_txt, (self.position[0] + (self.size_bg[0] / 3), self.position[1]))

    def change_text(self, new_text: str):
        self.text = new_text
        self.render_txt = self.font.render(self.text, False, self.color_text)
        self.screen.blit(self.render_txt, (self.position[0] + (self.size_bg[0] / 3), self.position[1]))

class Pedal: # Game Pedal

    pos: list or tuple = [0, 0]
    size: list or tuple = [0, 0]
    screen = None
    color: tuple or list = [255, 255, 255]
    key_control: list or tuple = (pg.K_w, pg.K_s)
    speed: int = 5
    score: int = 0

    def __init__(self, screen, size: tuple or list, position: tuple or list, color: tuple or list, control, speed: int):
        self.pos, self.size = position, size
        self.screen = screen
        self.color = color
        self.key_control = control
        self.speed = speed
        self.square = pg.Rect(self.pos, self.size)
        pg.draw.rect(self.screen, self.color, self.square)

    def change_pos(self, speed):
        self.pos[1] += speed
        self.square = pg.Rect(self.pos, self.size)

    def getKeyControlUp(self):
        return self.key_control[0]

    def getKeyControlDown(self):
        return self.key_control[1]

    def show(self):
        pg.draw.rect(self.screen, self.color, self.square)

class Ball: # Game Ball

    DEFAULT_POSITION: tuple or list = (0, 0)
    speed: list = [0, 0]
    size = (0, 0)
    screen = None

    def __init__(self, screen, ball_size: tuple or list, speed: list):
        self.screen = screen
        self.size = ball_size
        self.speed = speed
        middle_placement_x = (self.screen.get_size()[0] / 2) - (self.size[0] / 2)
        middle_placement_y = (self.screen.get_size()[1] / 2) - (self.size[1] / 2)
        self.DEFAULT_POSITION = (middle_placement_x, middle_placement_y)

    def behave(self):
        pass

# Frame Instantiate
win_size = (720, 480)
win_title, win_icon = "PONG!", "Ball.png"
clock = pg.time.Clock()
btn_size = (150, 35)
font_ComicSansMS = "Font\\comic.ttf"
pedal_size = (8, 150)

# All Colors
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

if __name__ == '__main__': # Main Program Run
    pg.init()
    MainMenu(win_size, win_title, win_icon)
    pg.quit()
    sys.exit()