#!/usr/bin/env python
"""
This game made with PyGame and Love
"""

import os
import sys
import random
import pygame as pg
import pygame_menu as pg_menu


class Game():
    '''
    Main game loop and parameters
    '''
    VERSION = 0.3
    MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
    DATA_DIR = os.path.join(MAIN_DIR, 'sources')
    ROOT_WINDOW_SIZE = (640, 640)
    BORDER_OFFSET = 32
    BORDER_WALL = pg.Rect(
            BORDER_OFFSET / 2,
            BORDER_OFFSET / 2,
            ROOT_WINDOW_SIZE[0] - BORDER_OFFSET,
            ROOT_WINDOW_SIZE[1] - BORDER_OFFSET)
    FPS = 24

    def __init__(self):
        '''
        Initialize our game with some additions
        '''
        pg.init()
        if not pg.font:
            print("Warning, fonts disabled")
            pg.font = None
        self.root_window = pg.display.set_mode(
                Game.ROOT_WINDOW_SIZE,
                pg.DOUBLEBUF)
        pg.display.set_caption(f'Rembo-Pacman v.{Game.VERSION}')
        pg.mouse.set_visible(False)
        self.run_state = False
        self.screen = None

        self.clock = pg.time.Clock()
        background_image = pg.image.load(
                os.path.join(Game.DATA_DIR, 'background.png')).convert()
        self.background = pg.transform.scale(
                background_image, Game.ROOT_WINDOW_SIZE)
        self.font = pg.font.SysFont(None, 48)
        self.kill_counter = 0

    def run(self) -> None:
        '''
        Run menu before main game, look at run_game()
        '''
        menu = self.create_menu()
        menu.mainloop(self.root_window)

    def run_game(self) -> None:
        '''
        Run main game loop
        '''
        self.run_state = True

        player = RemboPacman()
        player_sprite = pg.sprite.Group()
        player_sprite.add(player)
        enemy_sprites = pg.sprite.Group()
        enemy_sprites.add([Enemy() for i in range(4)])

        while self.run_state:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.run_state = False
                    sys.exit()

            self.root_window.blit(self.background, (0, 0))
            player.handle_move()
            for enemy in enemy_sprites:
                enemy.random_move()
                if enemy.rect.colliderect(player):
                    enemy.kill()
                    enemy_sprites.add(Enemy())
                    self.kill_counter += 1
            self.draw_kill_counter()
            enemy_sprites.update()
            player_sprite.update()
            player_sprite.draw(self.root_window)
            enemy_sprites.draw(self.root_window)
            pg.display.update()
            pg.display.flip()

            self.clock.tick(Game.FPS)
        pg.quit()

    def create_menu(self) -> pg_menu.Menu:
        '''
        Create simple game menu with help
        '''
        keybord_help = '''
            Help:
            Use arrow keys (up, down, left, right)
            for control your Pac-Man.
            You can only eat creeps
            '''
        menu = pg_menu.Menu(
                'Welcome to Rambo-Pac-Man',
                640,
                640,
                theme=pg_menu.themes.THEME_SOLARIZED)
        menu.add.text_input('Hit your Name :', default=' Mr.Gamer')
        menu.add.vertical_margin(20)
        menu.add.button('Play', self.run_game)
        menu.add.button('Quit', pg_menu.events.EXIT)
        menu.add.vertical_margin(20)
        menu.add.selector('Difficulty :', [('Hard NotImplemented other', 1)])
        menu.add.vertical_margin(20)
        menu.add.clock()
        menu.add.vertical_margin(20)
        menu.add.table('lol')
        menu.add.label(
                keybord_help,
                max_char=-1,
                font_size=24,
                align=pg_menu.locals.ALIGN_LEFT)
        return menu

    def draw_kill_counter(self):
        self.root_window.blit(
                self.font.render(
                    f'YOU KILL: {self.kill_counter}',
                    True,
                    'red'),
                (420, 32))

    @classmethod
    def scale_image(cls, image: pg.Surface, size: tuple) -> pg.Surface:
        '''
        Scaling image from any size
        '''
        return pg.transform.scale(image, size)


class RemboPacman(pg.sprite.Sprite):
    '''
    Pacman!
    '''
    def __init__(self):
        super().__init__()
        self.size = (32, 32)
        self.border_wall = Game.BORDER_WALL
        self.start_position = self.border_wall.center
        self.animate_direction = 'right'
        self.right_move_frames = [
                Game.scale_image(pg.image.load(os.path.join(
                    Game.DATA_DIR, 'pacman_right_0.png')), self.size),
                Game.scale_image(pg.image.load(os.path.join(
                    Game.DATA_DIR, 'pacman_right_1.png')), self.size),
                ]
        self.left_move_frames = [
                Game.scale_image(pg.image.load(os.path.join(
                    Game.DATA_DIR, 'pacman_left_0.png')), self.size),
                Game.scale_image(pg.image.load(os.path.join(
                    Game.DATA_DIR, 'pacman_left_1.png')), self.size),
                ]
        self.image = self.right_move_frames[0]
        self.rect = self.image.get_rect(center=self.start_position)

    def move_animation(self, direction) -> None:
        '''
        Not the best way for animate move but the most fastest
        '''
        if direction == 'right':
            if self.image == self.right_move_frames[0]:
                self.image = self.right_move_frames[1]
            else:
                self.image = self.right_move_frames[0]
        if direction == 'left':
            if self.image == self.left_move_frames[0]:
                self.image = self.left_move_frames[1]
            else:
                self.image = self.left_move_frames[0]

    def handle_move(self) -> None:
        """ Movement keys """
        move_step = 5
        key_input = pg.key.get_pressed()
        if key_input[pg.K_RIGHT]:
            self.rect.move_ip(move_step, 0)
            self.rect.clamp_ip(self.border_wall)
            if self.image in self.right_move_frames:
                self.animate_direction = 'right'
                self.move_animation(self.animate_direction)
            else:
                self.image = self.right_move_frames[0]
        if key_input[pg.K_DOWN]:
            self.rect.move_ip(0, move_step)
            self.rect.clamp_ip(self.border_wall)
            self.move_animation(self.animate_direction)
        if key_input[pg.K_LEFT]:
            self.rect.move_ip(-move_step, 0)
            self.rect.clamp_ip(self.border_wall)
            if self.image in self.left_move_frames:
                self.animate_direction = 'left'
                self.move_animation(self.animate_direction)
            else:
                self.image = self.left_move_frames[0]
        if key_input[pg.K_UP]:
            self.rect.move_ip(0, -move_step)
            self.rect.clamp_ip(self.border_wall)
            self.move_animation(self.animate_direction)


class Enemy(pg.sprite.Sprite):
    '''
    Passive enemy class. Can only be eating by player
    '''
    def __init__(self):
        super().__init__()
        self.clock = pg.time.Clock()
        self.time_counter = 0
        self.time_direction_counter = 0
        self.size = (random.randint(20, 40), random.randint(20, 40))
        self.border_wall = Game.BORDER_WALL
        self.start_position = (
                random.randint(32, 600),
                random.randint(32, 600))
        self.right_image = Game.scale_image(
                pg.image.load(os.path.join(Game.DATA_DIR, 'creep_right.png')),
                self.size)
        self.left_image = Game.scale_image(
                pg.image.load(os.path.join(Game.DATA_DIR, 'creep_left.png')),
                self.size)
        self.image = self.right_image
        self.rect = self.image.get_rect(center=self.start_position)
        self.direction = random.choice(['up', 'right', 'down', 'left'])

    def random_move(self) -> None:
        """ Creeps random move """
        time_passed = self.clock.tick()
        self.time_counter += time_passed
        self.time_direction_counter += time_passed
        if self.time_counter > 650:
            move_step = random.randint(10, 30)
            if self.time_direction_counter > 2400:
                self.direction = random.choice(['up', 'right', 'down', 'left'])
                self.time_direction_counter = 0
            match self.direction:
                case 'up':
                    self.rect.move_ip(0, move_step)
                    self.rect.clamp_ip(self.border_wall)
                case 'right':
                    self.rect.move_ip(move_step, 0)
                    self.rect.clamp_ip(self.border_wall)
                case 'down':
                    self.rect.move_ip(0, -move_step)
                    self.rect.clamp_ip(self.border_wall)
                case 'left':
                    self.rect.move_ip(-move_step, 0)
                    self.rect.clamp_ip(self.border_wall)
            self.time_counter = 0


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    game = Game()
    game.run()
