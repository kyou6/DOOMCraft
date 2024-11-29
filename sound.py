import pygame as pg
import random


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        
        # Load multiple sound variations
        self.shotgun_sounds = [
            pg.mixer.Sound(self.path + 'player_shoot1.ogg'),
            pg.mixer.Sound(self.path + 'player_shoot2.ogg'),
        ]
        
        self.npc_pain_sounds = [
            pg.mixer.Sound(self.path + 'npc_hit1.ogg'),
            pg.mixer.Sound(self.path + 'npc_hit2.ogg'),
            pg.mixer.Sound(self.path + 'npc_hit3.ogg'),
            pg.mixer.Sound(self.path + 'npc_hit4.ogg'),
        ]

        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.ogg')

        self.npc_shot_sounds = [
            pg.mixer.Sound(self.path + 'npc_shoot1.ogg'),
            pg.mixer.Sound(self.path + 'npc_shoot2.ogg'),
        ]

        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        pg.mixer.music.load(self.path + 'theme.mp3')
        pg.mixer.music.set_volume(0.3)

    def play_shotgun_sound(self):
        random.choice(self.shotgun_sounds).play()

    def play_npc_pain_sound(self):
        random.choice(self.npc_pain_sounds).play()

    def play_npc_shot_sound(self):
        random.choice(self.npc_shot_sounds).play()

    def update_volume(self, volume):
        # Update all sound effects volume
        for sounds in [self.shotgun_sounds, self.npc_pain_sounds, self.npc_shot_sounds]:
            for sound in sounds:
                sound.set_volume(volume)
        
        self.npc_death.set_volume(volume)
        self.player_pain.set_volume(volume)