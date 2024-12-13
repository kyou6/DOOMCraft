from sprite_object import *
import os


class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapons/shotgun/shotgun1.bmp', scale=3, animation_time=90):
        super().__init__(game=game, path=path, scale=1, animation_time=animation_time)
        self.images = deque(
            [pg.transform.scale(img, (128, 128))
             for img in self.images])
        self.weapon_scale = scale
        self.weapon_base_pos = (HALF_WIDTH - 32 * self.weapon_scale // 2, HEIGHT - 32 * self.weapon_scale)
        self.weapon_pos = self.weapon_base_pos
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        
        # Weapon properties
        self.weapons = {
            1: {'name': 'fist', 'damage': 20, 'animation_time': 90},
            2: {'name': 'pistol', 'damage': 30, 'animation_time': 90},
            3: {'name': 'shotgun', 'damage': 80, 'animation_time': 90},
            4: {'name': 'dbshotgun', 'damage': 120, 'animation_time': 100},
            5: {'name': 'chaingun', 'damage': 40, 'animation_time': 50},
            6: {'name': 'plasma', 'damage': 100, 'animation_time': 60},
            7: {'name': 'rocket', 'damage': 150, 'animation_time': 100},
            8: {'name': 'bfg', 'damage': 1000, 'animation_time': 200}
        }
        self.current_weapon = 2  # Default to pistol
        self.damage = self.weapons[self.current_weapon]['damage']
        self.load_weapon(self.current_weapon)

    def get_images(self, path):
        images = deque()
        weapon_name = path.split('/')[-1]
        # Look for files named weapon1.bmp through weapon5.bmp
        for i in range(1, 6):
            file_name = f'{weapon_name}{i}.bmp'
            full_path = os.path.join(path, file_name)
            if os.path.exists(full_path):
                # Load the image
                img = pg.image.load(full_path).convert()
                # Get the background color from top-left pixel
                bg_color = img.get_at((0, 0))
                # Set that color as transparent
                img.set_colorkey(bg_color, pg.RLEACCEL)
                images.append(img)
        return images

    def load_weapon(self, weapon_num):
        weapon = self.weapons[weapon_num]
        self.animation_time = weapon['animation_time']
        weapon_name = weapon['name']
        
        self.path = f'resources/sprites/weapons/{weapon_name}'
        self.images = self.get_images(self.path)
        
        # Scale images while maintaining transparency
        self.images = deque([])
        for img in self.get_images(self.path):
            bg_color = img.get_at((0, 0))
            scaled = pg.transform.scale(img, (32, 32))
            scaled.set_colorkey(bg_color, pg.RLEACCEL)  # Reapply colorkey after scaling
            self.images.append(scaled)
        
        if len(self.images) > 0:
            self.image = self.images[0]
        else:
            print(f"Warning: No images found for weapon {weapon_name}")
            
        self.num_images = len(self.images)
        self.damage = weapon['damage']
        
        self.frame_counter = 0
        self.reloading = False

    def switch_weapon(self, weapon_num):
        if weapon_num in self.weapons and weapon_num != self.current_weapon:
            self.current_weapon = weapon_num
            self.load_weapon(weapon_num)

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
        scaled = pg.transform.scale(self.images[0], (32 * self.weapon_scale, 32 * self.weapon_scale))
        bg_color = self.images[0].get_at((0, 0))
        scaled.set_colorkey(bg_color, pg.RLEACCEL)
        self.game.screen.blit(scaled, self.weapon_pos)

    @property
    def recoil(self):
        if self.reloading:
            return int(20 * (self.num_images - self.frame_counter) / self.num_images)
        return 0

    def update(self):
        self.check_animation_time()
        self.animate_shot()