import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 16
        self.digits = {
            '0': pg.image.load('resources/textures/digits/0.png').convert_alpha(),
            '1': pg.image.load('resources/textures/digits/1.png').convert_alpha(),
            '2': pg.image.load('resources/textures/digits/2.png').convert_alpha(),
            '3': pg.image.load('resources/textures/digits/3.png').convert_alpha(),
            '4': pg.image.load('resources/textures/digits/4.png').convert_alpha(),
            '5': pg.image.load('resources/textures/digits/5.png').convert_alpha(),
            '6': pg.image.load('resources/textures/digits/6.png').convert_alpha(),
            '7': pg.image.load('resources/textures/digits/7.png').convert_alpha(),
            '8': pg.image.load('resources/textures/digits/8.png').convert_alpha(),
            '9': pg.image.load('resources/textures/digits/9.png').convert_alpha(),
            '10': pg.image.load('resources/textures/digits/10.png').convert_alpha(),
        }
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)
        
        # Death screen elements
        self.death_screen_active = False
        self.buttons = []
        self.font = pg.font.Font(FONT_PATH, MENU_FONT_SIZE)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        if not self.game.paused and not self.death_screen_active:
            self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.death_screen_active = True
        self.game.paused = True
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        self.draw_death_screen()

    def draw_death_screen(self):
        # Draw dark semi-transparent background
        s = pg.Surface(RES)
        s.fill((0, 0, 0))
        s.set_alpha(180)  # More opaque than menu background
        self.screen.blit(s, (0, 0))

        # Draw "YOU DIED" text
        self.screen.blit(self.game_over_image, (0, 0))  # Draw the game over image

        # Draw buttons
        self.buttons.clear()
        button_y = HALF_HEIGHT + 50
        spacing = 80

        # Respawn button
        respawn_text = self.font.render('Respawn', True, (255, 255, 255))
        respawn_rect = respawn_text.get_rect(center=(HALF_WIDTH, button_y))
        self.screen.blit(respawn_text, respawn_rect)
        self.buttons.append(('Respawn', respawn_rect))

        # Quit button
        quit_text = self.font.render('Quit Game', True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(HALF_WIDTH, button_y + spacing))
        self.screen.blit(quit_text, quit_rect)
        self.buttons.append(('Quit Game', quit_rect))

        self.death_screen_active = True

    def handle_death_screen_click(self, pos):
        for button_text, button_rect in self.buttons:
            if button_rect.collidepoint(pos):
                if button_text == 'Respawn':
                    self.death_screen_active = False
                    self.game.new_game()
                    self.game.paused = False
                    pg.mouse.set_visible(False)
                    pg.event.set_grab(True)
                elif button_text == 'Quit Game':
                    pg.quit()
                    exit()

    def draw_player_health(self):
        health = max(0, self.game.player.health)
        health_str = str(health)

        # Set the initial position for the first digit
        initial_x_position = 50
        y_position = 50

        # Define the width of each digit texture
        digit_width = self.digit_size
        spacing = 60

        for i, char in enumerate(health_str):
            if char in self.digits:
                # Calculate the x position for each digit with spacing
                x_position = initial_x_position + (i * (digit_width + spacing))
                self.screen.blit(self.digits[char], (x_position, y_position))
            else:
                print(f"Warning: Character '{char}' not found in digits dictionary.")

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        if not self.game.paused:
            self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }

    def draw_menu(self):
        # Example of drawing menu items with the custom font
        menu_text = self.font.render('Main Menu', True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 100))
        self.screen.blit(menu_text, menu_rect)

        # Add more menu items as needed
        start_text = self.font.render('Start Game', True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT))
        self.screen.blit(start_text, start_rect)

        quit_text = self.font.render('Quit', True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 100))
        self.screen.blit(quit_text, quit_rect)