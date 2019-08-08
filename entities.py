import pygame as pg
import math
import random
import weapons


class MainChar(pg.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        settings.game_sprites.add(self)
        settings.mc_sprites.add(self)
        settings.creatures_sprites.add(self)
        self.image = pg.image.load('assets/main_char.png').convert()
        self.rect = self.image.get_rect(center=[settings.resolution[0]/2, settings.resolution[1]/2])
        self.speed = 3
        self.hp = 5
        self.weapon = weapons.Pistol()

    def update(self, settings, dt):
        if self.hp <= 0:
            settings.game = False
        self.weapon.update(dt)

    def get_damage(self, damage):
        self.hp -= damage


class Enemy(pg.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        settings.game_sprites.add(self)
        settings.enemy_sprites.add(self)
        settings.creatures_sprites.add(self)
        self.speed = 1.5
        self.hp = 4
        self.damage = 1
        self.image = pg.image.load('assets/enemy.png')
        self.rect = self.image.get_rect(center=[random.randint(0, settings.resolution[0]),
                                                random.randint(0, settings.resolution[1])])

    def update(self, settings, dt):
        if self.hp <= 0:
            settings.score += 1
            self.kill()
        self.move_to_player(settings.mc_sprites.sprites()[0])

    def get_damage(self, damage):
        self.hp -= damage

    def move_to_player(self, mc):
        v = [mc.rect[0] - self.rect[0], mc.rect[1] - self.rect[1]]
        mv = math.sqrt(v[0]**2 + v[1]**2)
        uv = [v[0] / mv, v[1] / mv]
        self.rect.move_ip(uv[0]*self.speed, uv[1]*self.speed)


class Wall(pg.sprite.Sprite):
    def __init__(self, settings, rotation):
        super(Wall, self).__init__()
        settings.wall_sprites.add(self)
        settings.game_sprites.add(self)
        if rotation == 'vertical':
            self.image = pg.image.load('assets/horizontal_wall.png')
        else:
            self.image = pg.image.load('assets/wall.png')
        self.rect = self.image.get_rect()


class Bullet(pg.sprite.Sprite):
    def __init__(self, damage, speed, mc_pos, uv, spread):
        super().__init__()
        self.damage = damage
        self.speed = speed
        self.image = pg.image.load('assets/bullet.png')
        self.rect = self.image.get_rect(center=[mc_pos[0] + mc_pos[2]/2,
                                                mc_pos[1] + mc_pos[3]/2])
        self.uv = [(uv[0]+spread) * speed, (uv[1]-spread) * speed]

    def update(self, settings, dt):
        # Move in direction of mouse
        self.rect.move_ip(self.uv)

        # Kill if out of screen
        if self.rect[0] < 0 or self.rect[0] > settings.resolution[0]:
            self.kill()
        if self.rect[1] < 0 or self.rect[1] > settings.resolution[1]:
            self.kill()


class WeaponButton(pg.sprite.Sprite):
    def __init__(self, settings, text, weapon):
        super(WeaponButton, self).__init__()
        settings.menu_sprites.add(self)
        settings.button_sprites.add(self)

        self.weapon = weapon
        self.cost = weapon.cost
        self.text = text

        self.rect = pg.Rect(100, 100, 150, 40)
        self.image = pg.Surface((150, 40))
        self.image.fill([255, 255, 255])

    def pressed(self, settings, mc):
        if settings.score >= self.cost:
            settings.score -= self.cost
            mc.weapon = self.weapon
            return True
        else:
            return False


class StatButton(pg.sprite.Sprite):
    def __init__(self, settings, text, stat, cost, amount):
        super(StatButton, self).__init__()
        settings.menu_sprites.add(self)
        settings.button_sprites.add(self)

        self.stat = stat
        self.text = text
        self.cost = cost
        self.amount = amount

        self.rect = pg.Rect(100, 100, 150, 40)
        self.image = pg.Surface((150, 40))
        self.image.fill([255, 255, 255])

    def pressed(self, settings, mc):
        if settings.score >= self.cost:
            settings.score -= self.cost
            if self.stat == 'speed':
                mc.speed += self.amount
            elif self.stat == 'health':
                mc.hp += self.amount
            return True
        else:
            return False
