from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=3, animation_time=90):
        super().__init__(game=game, path=path, scale=1, animation_time=animation_time)
        self.images = deque(
            [pg.transform.scale(img, (32, 32))
             for img in self.images])
        self.weapon_scale = scale
        self.weapon_base_pos = (HALF_WIDTH - 32 * self.weapon_scale // 2, HEIGHT - 32 * self.weapon_scale)
        self.weapon_pos = self.weapon_base_pos
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 80

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
            self.weapon_pos = self.weapon_base_pos[0], self.weapon_base_pos[1] + self.recoil

    def draw(self):
        weapon_surface = pg.transform.scale(self.images[0], (32 * self.weapon_scale, 32 * self.weapon_scale))
        self.game.screen.blit(weapon_surface, self.weapon_pos)

    @property
    def recoil(self):
        if self.reloading:
            return int(20 * (self.num_images - self.frame_counter) / self.num_images)
        return 0

    def update(self):
        self.check_animation_time()
        self.animate_shot()