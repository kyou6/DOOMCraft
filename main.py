import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from menu import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.paused = False
        self.new_game()
        self.menu = Menu(self)

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self, scale=16)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def update(self):
        if not self.paused:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
            self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()
        if self.menu.active:
            self.menu.draw()
        if self.object_renderer.death_screen_active:
            self.object_renderer.draw_death_screen()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if not self.object_renderer.death_screen_active:
                        self.menu.active = not self.menu.active
                        self.paused = self.menu.active
                        pg.mouse.set_visible(self.menu.active)
                        pg.event.set_grab(not self.menu.active)
                elif (event.key == pg.K_RETURN and pg.key.get_mods() & pg.KMOD_ALT) or event.key == pg.K_F11:
                    self.toggle_fullscreen()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.object_renderer.death_screen_active:
                    self.object_renderer.handle_death_screen_click(pg.mouse.get_pos())
                elif self.menu.active:
                    self.menu.handle_click(pg.mouse.get_pos())
            elif event.type == pg.MOUSEBUTTONUP and self.menu.active:
                self.menu.handle_mouse_up()
            elif event.type == pg.MOUSEMOTION and self.menu.active and self.menu.active_slider:
                self.menu.update_slider(event.pos[0])
            elif event.type == self.global_event:
                self.global_trigger = True
            if not self.paused:
                self.player.single_fire_event(event)

    def toggle_fullscreen(self):
        if self.menu.fullscreen:
            # Get the current display resolution
            display_info = pg.display.Info()
            max_width, max_height = display_info.current_w, display_info.current_h
            
            # Calculate the aspect ratio of the game
            game_aspect_ratio = WIDTH / HEIGHT
            
            # Calculate new dimensions while retaining aspect ratio
            if max_width / max_height > game_aspect_ratio:
                # Monitor is wider than the game aspect ratio
                new_height = max_height
                new_width = int(new_height * game_aspect_ratio)
            else:
                # Monitor is taller than the game aspect ratio
                new_width = max_width
                new_height = int(new_width / game_aspect_ratio)

            # Set the display mode to fullscreen with the calculated resolution
            pg.display.set_mode((new_width, new_height), pg.FULLSCREEN)
        else:
            # Set back to windowed mode with the original resolution
            pg.display.set_mode(RES)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
