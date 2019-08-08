import math
import random
import entities


class Weapon:
    def __init__(self, cost, ammo, cooldown, reload, damage, speed, shots, spread, auto):
        self.shots = shots
        self.cost = cost
        self.max_ammo = ammo
        self.ammo = ammo
        self.max_cooldown = cooldown
        self.cooldown = cooldown
        self.reload_cooldown = reload
        self.auto = auto
        self.damage = damage
        self.speed = speed
        self.shooting = False
        self.spread = spread

    def update(self, dt):
        self.cooldown -= dt
        if self.cooldown < 0:
            self.cooldown = 0

    def update_mouse_input(self, mouse_input, mouse_pos, mc_pos, settings):
        if mouse_input[2]:
            self.special(mouse_pos, mc_pos, settings)
        elif self.auto:
            if mouse_input[0] and self.auto and self.ammo > 0 >= self.cooldown:
                self.shoot(mouse_pos, mc_pos, settings)
            elif mouse_input[0] and self.ammo <= 0:
                pass    # Out of ammo
        else:   # self.auto is False
            if mouse_input[0] and self.shooting is False and self.ammo > 0 >= self.cooldown:
                self.shoot(mouse_pos, mc_pos, settings)
                self.shooting = True
            elif mouse_input[0] and self.ammo <= 0:
                pass    # Out of ammo
            if mouse_input[0] == 0:
                self.shooting = False

    def shoot(self, mouse_pos, mc_pos, settings):
        self.ammo -= 1
        self.cooldown = self.max_cooldown

        for i in range(self.shots):
            spread = random.random() * self.spread * random.choice([-1, 1])
            v = [mouse_pos[0] - mc_pos[0], mouse_pos[1] - mc_pos[1]]
            mv = math.sqrt(v[0]**2 + v[1]**2)
            uv = [(v[0] / mv), (v[1] / mv)]
            new_bullet = entities.Bullet(self.damage, self.speed, mc_pos, uv, spread)
            settings.game_sprites.add(new_bullet)
            settings.bullet_sprites.add(new_bullet)

    def reload(self):
        print('Reloading!')
        self.ammo = self.max_ammo
        self.cooldown = self.reload_cooldown


class Pistol(Weapon):
    def __init__(self):
        super(Pistol, self).__init__(0, 6, 0.25, 1.5, 5, 10, 1, 0.0, False)

    def special(self, mouse_pos, mc_pos, game_sprites):
        while self.ammo > 0:
            self.shoot(mouse_pos, mc_pos, game_sprites)


class Rifle(Weapon):
    def __init__(self):
        super(Rifle, self).__init__(10, 25, 0.15, 2, 2, 8, 1, 0.1, True)

    def special(self, mouse_pos, mc_pos, game_sprites):
        pass


class Shotgun(Weapon):
    def __init__(self):
        super(Shotgun, self).__init__(5, 8, 0.5, 1.5, 3, 10, 6, 0.3, False)

    def special(self, mouse_pos, mc_pos, game_sprites):
        pass


class MachineGun(Weapon):
    def __init__(self):
        super(MachineGun, self).__init__(30, 200, 0.05, 3, 1, 10, 2, 0.3, True)

    def special(self, mouse_pos, mc_pos, game_sprites):
        if self.cooldown <= 0:
            self.shots = self.ammo
            self.spread = 0.7
            self.shoot(mouse_pos, mc_pos, game_sprites)
            self.ammo = 0
            self.shots = 2
            self.spread = 0.3
