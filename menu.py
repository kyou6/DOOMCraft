import pygame as pg
from settings import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.buttons = []
        self.current_menu = 'main'
        self.font = pg.font.Font(FONT_PATH, MENU_FONT_SIZE)
        self.small_font = pg.font.Font(FONT_PATH, MENU_SMALL_FONT_SIZE)
        
        # Settings values
        self.fullscreen = False
        self.music_volume = 1.0
        self.sound_volume = 1.0
        
        # Slider states
        self.active_slider = None
        self.sliders = {}
        
        # Slider ranges
        self.slider_ranges = {
            'Music Volume': (0, 1.0),
            'Sound Volume': (0, 1.0)
        }
        
        # Difficulty settings
        self.difficulty_presets = {
            #'Dev': [100.0, 100.0],
            'Easy': [0.4, 0.4],
            'Normal': [1.0, 1.0],
            'Hard': [2.0, 2.0],
            'Extreme': [10.0, 10.0]
        }
        self.current_difficulty = 'Normal'

    def draw(self):
        if not self.active:
            return

        s = pg.Surface(RES)
        s.fill((0, 0, 0))
        s.set_alpha(128)
        self.game.screen.blit(s, (0, 0))

        if self.current_menu == 'main':
            self.draw_main_menu()
        elif self.current_menu == 'settings':
            self.draw_settings_menu()
        elif self.current_menu == 'difficulty':
            self.draw_difficulty_menu()

    def draw_main_menu(self):
        menu_items = ['Resume Game', 'Settings', 'Difficulty', 'Quit Game']
        for i, item in enumerate(menu_items):
            text = self.font.render(item, True, (255, 255, 255))
            pos = (HALF_WIDTH - text.get_width() // 2, HALF_HEIGHT - 100 + i * 80)
            self.game.screen.blit(text, pos)
            self.buttons.append((item, pg.Rect(pos[0], pos[1], text.get_width(), text.get_height())))

    def draw_settings_menu(self):
        self.buttons.clear()
        self.sliders.clear()
        
        # Title
        title = self.font.render('Settings', True, (255, 255, 255))
        self.game.screen.blit(title, (HALF_WIDTH - title.get_width() // 2, 100))

        # Settings options
        y_pos = 250
        spacing = 80

        # Fullscreen toggle
        fullscreen_text = self.small_font.render(f'Fullscreen: {"On" if self.fullscreen else "Off"}', True, (255, 255, 255))
        fullscreen_pos = (HALF_WIDTH - fullscreen_text.get_width() // 2, y_pos)
        self.game.screen.blit(fullscreen_text, fullscreen_pos)
        self.buttons.append(('Fullscreen', pg.Rect(fullscreen_pos[0], fullscreen_pos[1], 
                                                 fullscreen_text.get_width(), fullscreen_text.get_height())))
        y_pos += spacing

        # Music Volume
        self.draw_slider('Music Volume', self.music_volume, y_pos)
        y_pos += spacing

        # Sound Volume
        self.draw_slider('Sound Volume', self.sound_volume, y_pos)
        y_pos += spacing

        # Back button
        back = self.font.render('Back', True, (255, 255, 255))
        back_pos = (HALF_WIDTH - back.get_width() // 2, y_pos)
        self.game.screen.blit(back, back_pos)
        self.buttons.append(('Back', pg.Rect(back_pos[0], back_pos[1], back.get_width(), back.get_height())))

    def draw_slider(self, text, value, y_pos):
        # Get the range for this slider
        min_val, max_val = self.slider_ranges.get(text, (0, 100))
        
        # Calculate the normalized value (0-100) for display
        normalized_value = ((value - min_val) / (max_val - min_val)) * 100
        
        # Display value
        display_value = f'{int(normalized_value)}'
        text_surface = self.small_font.render(f'{text}: {display_value}', True, (255, 255, 255))
        self.game.screen.blit(text_surface, (HALF_WIDTH - 200, y_pos))
        
        # Draw slider bar
        slider_rect = pg.Rect(HALF_WIDTH - 150, y_pos + 30, 300, 10)
        pg.draw.rect(self.game.screen, (100, 100, 100), slider_rect)
        pg.draw.rect(self.game.screen, (255, 255, 255), 
                    (HALF_WIDTH - 150, y_pos + 30, 300 * (normalized_value/100), 10))
        
        # Store slider info for interaction
        self.sliders[text] = {
            'rect': slider_rect,
            'value': value,
            'y_pos': y_pos
        }

    def draw_difficulty_menu(self):
        title = self.font.render('Difficulty', True, (255, 255, 255))
        self.game.screen.blit(title, (HALF_WIDTH - title.get_width() // 2, 100))

        y_pos = 250
        for difficulty in self.difficulty_presets.keys():
            color = (255, 255, 0) if difficulty == self.current_difficulty else (255, 255, 255)
            text = self.font.render(difficulty, True, color)
            pos = (HALF_WIDTH - text.get_width() // 2, y_pos)
            self.game.screen.blit(text, pos)
            self.buttons.append((difficulty, pg.Rect(pos[0], pos[1], text.get_width(), text.get_height())))
            y_pos += 80

        back = self.font.render('Back', True, (255, 255, 255))
        back_pos = (HALF_WIDTH - back.get_width() // 2, y_pos)
        self.game.screen.blit(back, back_pos)
        self.buttons.append(('Back', pg.Rect(back_pos[0], back_pos[1], back.get_width(), back.get_height())))

    def handle_click(self, pos):
        # Check for slider interaction
        if self.current_menu == 'settings':
            for slider_name, slider_info in self.sliders.items():
                if slider_info['rect'].collidepoint(pos):
                    self.active_slider = slider_name
                    self.update_slider(pos[0])
                    return

        # Check for button clicks
        for button_text, button_rect in self.buttons:
            if button_rect.collidepoint(pos):
                self.handle_button(button_text)
        self.buttons.clear()

    def handle_mouse_up(self):
        self.active_slider = None

    def update_slider(self, x_pos):
        if not self.active_slider or self.active_slider not in self.sliders:
            return

        slider_info = self.sliders[self.active_slider]
        slider_rect = slider_info['rect']
        
        # Calculate normalized value (0-1)
        normalized_value = (x_pos - slider_rect.left) / slider_rect.width
        normalized_value = max(0, min(1, normalized_value))

        # Get the range for this slider
        min_val, max_val = self.slider_ranges[self.active_slider]
        
        # Calculate actual value based on range
        actual_value = min_val + (max_val - min_val) * normalized_value

        # Update the appropriate setting
        if self.active_slider == 'Music Volume':
            self.music_volume = actual_value
            pg.mixer.music.set_volume(self.music_volume)
        elif self.active_slider == 'Sound Volume':
            self.sound_volume = actual_value
            self.game.sound.update_volume(self.sound_volume)

    def handle_button(self, button_text):
        if button_text == 'Resume Game':
            self.active = False
            self.game.paused = False
            pg.mouse.set_visible(False)
            pg.event.set_grab(True)
        elif button_text == 'Settings':
            self.current_menu = 'settings'
        elif button_text == 'Difficulty':
            self.current_menu = 'difficulty'
        elif button_text == 'Quit Game':
            pg.quit()
            exit()
        elif button_text == 'Back':
            self.current_menu = 'main'
        elif button_text == 'Fullscreen':
            self.toggle_fullscreen()
        elif button_text in self.difficulty_presets:
            self.current_difficulty = button_text
            # Apply difficulty settings here

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            pg.display.set_mode(RES, pg.FULLSCREEN)
        else:
            pg.display.set_mode(RES)

    def handle_keydown(self, event):
        if event.key in (pg.K_F11, pg.K_RETURN) and event.mod & pg.KMOD_ALT:
            self.toggle_fullscreen()