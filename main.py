#!/usr/bin/env python
"""
Made with PyGame and Love
"""

import os
import random
import pygame as pg


class Game():
    '''
    Our game logic
    '''
    MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
    DATA_DIR = os.path.join(MAIN_DIR, 'sources')
    ROOT_WINDOW_SIZE = (640, 640)
    FPS = 30

    def __init__(self):
        '''
        Create our game
        '''
        pg.init()
        self.root_window = pg.display.set_mode(
                Game.ROOT_WINDOW_SIZE,
                pg.DOUBLEBUF)
        pg.display.set_caption('Rembo-Pacman')
        pg.mouse.set_visible(False)
        self.run_state = False
        self.screen = None

        self.clock = pg.time.Clock()
        background_image = pg.image.load(
                os.path.join(Game.DATA_DIR, 'background.png')).convert()
        background_image.set_alpha(100)
        self.background = pg.transform.scale(
                background_image, Game.ROOT_WINDOW_SIZE)

    def run(self):
        '''
        Run main game loop
        '''
        self.run_state = True
        if not pg.font:
            print("Warning, fonts disabled")
        if not pg.mixer:
            print("Warning, sound disabled")

        sprites = pg.sprite.Group()
        player = RemboPacman()
        sprites.add(player)

        while self.run_state:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.run_state = False

            self.root_window.blit(self.background, (0,0))
            player.handle_move()
            sprites.draw(self.root_window)
            pg.display.flip()
            self.clock.tick(Game.FPS)
        pg.quit()


class RemboPacman(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = (32,32)
        self.start_position = [i/2 for i in Game.ROOT_WINDOW_SIZE]
        self.image = pg.image.load(
                os.path.join(Game.DATA_DIR, 'pacman_left_0.png')).convert_alpha()
        self.image = pg.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect(center=self.start_position)

        self.right_move_animation = []
        self.left_move_animation = []

    def load_images(self):
        pass

    def handle_move(self):
        """ Movement keys """
        move_step = 10
        key_input = pg.key.get_pressed()
        if key_input[pg.K_RIGHT]:
            if self.rect.x < Game.ROOT_WINDOW_SIZE[0] - self.size[0]:
                self.rect.x += move_step
        if key_input[pg.K_DOWN]:
            if self.rect.y < Game.ROOT_WINDOW_SIZE[1] - self.size[0]:
                self.rect.y += move_step
        if key_input[pg.K_LEFT]:
            if self.rect.x > 0:
                self.rect.x -= move_step
        if key_input[pg.K_UP]:
            if self.rect.y > 0:
                self.rect.y -= move_step


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        size = (32, 32)
        pass

# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    game = Game()
    game.run()
