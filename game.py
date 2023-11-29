import pygame as pg
from sprites import *
import random
pg.init() # starter pygame modul
 
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)


screen = pg.display.set_mode((2560,1440)) # lager spill vindu, 800x600
clock = pg.time.Clock()
  
font_cs30 = pg.font.SysFont("Comic Sans", 30)
font_times40 = pg.font.SysFont("Times New Roman", 40)
 
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()
big_enemies = pg.sprite.Group()
enemies_special = pg.sprite.Group()
 
player = Player(all_sprites, enemies, big_enemies, enemies_special) # lager 1 kopi av Player class
all_sprites.add(player) # legg til player i gruppen

playing = True
while playing: # game loop
    clock.tick(120)
    #print("FPS: ", i)
    for event in pg.event.get():
        if event.type == pg.QUIT: # hvis vi trykker på krysset i spillvinduet
            playing = False
            pg.quit()


    # spawning av flere enemies
    if len(enemies) < 40:
        new_enemy = Enemy()
        new_enemy2 = Enemy2()
        new_enemy3 = Enemy3()
        new_enemy4 = Enemy4()
        all_sprites.add(new_enemy2) 
        enemies.add(new_enemy2)
        all_sprites.add(new_enemy3)
        enemies.add(new_enemy3)
        all_sprites.add(new_enemy4)
        enemies.add(new_enemy4)
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)


  
    if len(big_enemies) < 1:
        new_big_enemy = Big_enemy()
        all_sprites.add(new_big_enemy)
        big_enemies.add(new_big_enemy)
        enemies.add(new_big_enemy)


    if len(enemies_special) < 3:
        new_enemy_special = Enemy_special()
        all_sprites.add(new_enemy_special)
        enemies.add(new_enemy_special)
        enemies_special.add(new_enemy_special)                  


    
    # oppdater alle sprites i all_sprites gruppen
    all_sprites.update()
 
    enemies_hit = pg.sprite.spritecollide(player, enemies, True)
    if enemies_hit:
        #player.hp -= 10
        player.take_dmg(enemies_hit[0].damage)
 
        print(player.hp)

    enemies_hit2 = pg.sprite.spritecollide(player, big_enemies, True)
    if enemies_hit2:
        #player.hp -= 20
        player.take_dmg(enemies_hit2[0].damage)

        print(player.hp)

    enemies_hit3 = pg.sprite.spritecollide(player, enemies_special, True)
    if enemies_hit3:
        #player.hp -= 10                
        player.take_dmg(enemies_hit3[0].damage)
 
        print(player.hp)

    hp_text = font_times40.render(f"HP: {player.hp}", False, (RED))
 
    # tegn bakgrunn og alle sprites
    screen.blit(bg_image,(0,0))
    all_sprites.draw(screen)

    screen.blit(hp_text, (10,10))


    pg.display.update() 