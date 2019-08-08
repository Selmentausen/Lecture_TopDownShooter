import pygame as pg


class Settings:
    def __init__(self):
        # Game settings
        self.score = 30
        self.font = pg.font.SysFont('Arial', 26)
        self.game = True
        self.menu = -1

        # Display settings
        self.resolution = [800, 600]
        self.background = pg.image.load('assets/background.png')
        self.background_rect = self.background.get_rect()

        # Player controls
        self.mc_controls = {'up': pg.K_w, 'down': pg.K_s, 'left': pg.K_a,
                            'right': pg.K_d, 'reload': pg.K_r, 'rifle': pg.K_u,
                            'menu': pg.K_m}

        # Sprite groups
        self.game_sprites = pg.sprite.Group()
        self.menu_sprites = pg.sprite.Group()
        self.button_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.mc_sprites = pg.sprite.Group()
        self.wall_sprites = pg.sprite.Group()
        self.creatures_sprites = pg.sprite.Group()

        # TEST
        self.test_array = []