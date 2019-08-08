import pygame as pg
import random
import entities


def setup_walls(settings):
    [entities.Wall(settings, 'horizontal') for i in range(4)]
    [entities.Wall(settings, 'vertical') for i in range(4)]
    settings.wall_sprites.sprites()[0].rect.center = (300, 200)
    settings.wall_sprites.sprites()[1].rect.center = (300, 400)
    settings.wall_sprites.sprites()[2].rect.center = (500, 200)
    settings.wall_sprites.sprites()[3].rect.center = (500, 400)
    settings.wall_sprites.sprites()[4].rect.center = (300, 200)
    settings.wall_sprites.sprites()[5].rect.center = (300, 400)
    settings.wall_sprites.sprites()[6].rect.center = (500, 200)
    settings.wall_sprites.sprites()[7].rect.center = (500, 400)


def handle_collisions(settings, mc):
    bullet_enemy = pg.sprite.groupcollide(settings.bullet_sprites, settings.enemy_sprites, True, False)
    if bullet_enemy:
        for bullet, enemy in bullet_enemy.items():
            enemy[0].get_damage(bullet.damage)

    pg.sprite.groupcollide(settings.bullet_sprites, settings.wall_sprites, True, False)
    creatures_wall = pg.sprite.groupcollide(settings.creatures_sprites, settings.wall_sprites, False, False)
    if creatures_wall:
        _side_collisions(creatures_wall)
    mc_enemy = pg.sprite.groupcollide(settings.mc_sprites, settings.enemy_sprites, False, True)
    if mc_enemy:
        for mc, enemies in mc_enemy.items():
            for enemy in enemies:
                mc.get_damage(enemy.damage)


def _side_collisions(obj_wall):
    for obj, walls in obj_wall.items():
        for wall in walls:
            if wall.rect.collidepoint(obj.rect.midbottom):
                obj.rect.move_ip(0, wall.rect[1] - obj.rect.bottom)
            if wall.rect.collidepoint(obj.rect.midtop):
                obj.rect.move_ip(0, wall.rect.bottom - obj.rect[1])
            if wall.rect.collidepoint(obj.rect.midright):
                obj.rect.move_ip(wall.rect[0] - obj.rect.right, 0)
            if wall.rect.collidepoint(obj.rect.midleft):
                obj.rect.move_ip(wall.rect.right - obj.rect[0], 0)


def spawn_enemies(settings):
    if not settings.enemy_sprites:
        [entities.Enemy(settings) for i in range(0, random.randint(5, 15))]


def update_widgets(settings, mc, screen):
    health = settings.font.render('Health: ' + str(mc.hp), True, (0, 255, 0))
    gun = settings.font.render(str(type(mc.weapon).__name__), False, (0, 255, 0))
    ammo = settings.font.render('ammo: ' + str(mc.weapon.ammo), False, (0, 255, 0))
    cooldown = settings.font.render('cooldown: ' + str(mc.weapon.cooldown)[:3], False, (0, 255, 0))
    score = settings.font.render('score: ' + str(settings.score), False, (0, 255, 0))
    screen.blit(health, health.get_rect())
    screen.blit(gun, gun.get_rect().move(0, 26))
    screen.blit(ammo, ammo.get_rect().move(gun.get_rect().width + 5, 26))
    screen.blit(cooldown, cooldown.get_rect().move(0, 52))
    screen.blit(score, score.get_rect().move(0, 78))
    if settings.menu == 1:
        for button in settings.button_sprites:
            button_text = settings.font.render(button.text, False, (0, 0, 0))
            screen.blit(button_text, button.rect)


def handle_input(settings, mc):
    keys = pg.key.get_pressed()
    if settings.menu != 1:
        if keys[settings.mc_controls['up']]:
            mc.rect.move_ip(0, -mc.speed)
        if keys[settings.mc_controls['down']]:
            mc.rect.move_ip(0, mc.speed)
        if keys[settings.mc_controls['left']]:
            mc.rect.move_ip(-mc.speed, 0)
        if keys[settings.mc_controls['right']]:
            mc.rect.move_ip(mc.speed, 0)
        if keys[settings.mc_controls['reload']]:
            mc.weapon.reload()

    mouse = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()
    if settings.menu == 1:
        for button in settings.button_sprites:
            if button.rect.collidepoint(mouse_pos):
                if mouse[0]:
                    if button.pressed(settings, mc):
                        settings.menu *= -1
    else:
        mc.weapon.update_mouse_input(mouse, mouse_pos, mc.rect, settings)

