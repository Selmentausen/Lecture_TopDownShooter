import pygame as pg
import weapons
import settings as st
import entities
import event_handler

pg.init()
settings = st.Settings()
clock = pg.time.Clock()

screen = pg.display.set_mode(settings.resolution)
pg.display.set_caption('Top Down Survival')

mc = entities.MainChar(settings)
mc.rect.center = (mc.rect.center[0] + (mc.speed*1), mc.rect.center[1])

buttons = [entities.WeaponButton(settings, 'Pistol', weapons.Pistol()),
           entities.WeaponButton(settings, 'Shotgun', weapons.Shotgun()),
           entities.WeaponButton(settings, 'Rifle', weapons.Rifle()),
           entities.WeaponButton(settings, 'Machine Gun', weapons.MachineGun()),
           entities.StatButton(settings, 'Speed', 'speed', 5, 0.5),
           entities.StatButton(settings, 'Health', 'health', 2, 1)]
buttons[1].rect.move_ip(0, 50)
buttons[2].rect.move_ip(0, 100)
buttons[3].rect.move_ip(0, 150)
buttons[4].rect.move_ip(200, 0)
buttons[5].rect.move_ip(200, 50)
event_handler.setup_walls(settings)


while settings.game:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            settings.game = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                settings.game = False
            if event.key == settings.mc_controls['menu']:
                settings.menu *= -1
    event_handler.handle_input(settings, mc)
    if settings.menu == 1:
        screen.fill([255, 255, 0])
        settings.menu_sprites.draw(screen)
    else:
        screen.blit(settings.background, settings.background_rect)
        event_handler.handle_collisions(settings, mc)
        event_handler.spawn_enemies(settings)
        settings.game_sprites.update(settings, clock.get_time()/1000)     # (settings, delta_time)
        settings.game_sprites.draw(screen)
    event_handler.update_widgets(settings, mc, screen)
    pg.display.update()
    clock.tick(60)
