import pygame as pg
import random
 
player_image = pg.image.load("images/idle_1.png")

enemy_image = pg.image.load("images/Shaman_medaljong.png") 
enemy_image = pg.transform.scale(enemy_image,(200,150))
enemy2_image = pg.image.load("images/Truls.png")
enemy2_image = pg.transform.scale(enemy2_image,(200,150))
enemy3_image = pg.image.load("images/Håvard_baka.png")
enemy3_image = pg.transform.scale(enemy3_image,(200,150))
enemy4_image = pg.image.load("images/Nikcocado_scooter.png")
enemy4_image = pg.transform.scale(enemy4_image,(200,150))
big_enemy_image = pg.image.load("images/Nikocado avocado.png")
big_enemy_image = pg.transform.scale(big_enemy_image,(500,500))
bg_image = pg.image.load("images/Shaman durek.jpg")
bg_image = pg.transform.scale(bg_image,(2560,1440))
special_enemy_image = pg.image.load("images/Nikcocado avocado rocket ride.png")
special_enemy_image = pg.transform.scale(special_enemy_image,(600,450))


STANDING = pg.image.load("images/idle_1.png")
STANDING2 = pg.image.load("images/idle_2.png")
STANDING3 = pg.image.load("images/idle_3.png")
STANDING4 = pg.image.load("images/idle_4.png")
STANDING5 = pg.image.load("images/idle_5.png")
STANDING6 = pg.image.load("images/idle_6.png")
STANDING7 = pg.image.load("images/idle_7.png")
STANDING8 = pg.image.load("images/idle_8.png")


ranged_image = pg.image.load("images/Thick bullet.png") 
ranged_image = pg.transform.scale(ranged_image,(30,10))
Big_ranged_image = pg.image.load("images/Bullet bill.png")


class Player(pg.sprite.Sprite):
    def __init__(self, all_sprites, enemies, big_enemies, enemies_special): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.image = player_image
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pos_x = 200
        self.pos_y = 720
        self.speed = 10
        self.hp = 100
        self.all_sprites = all_sprites
        self.enemies = enemies
        self.big_enemies = big_enemies
        self.enemies_special = enemies_special
        self.last_attack = 200
        self.attack_interval = 500
        self.attack_cooldown = 0
        self.attack_cooldown2 = 0
        self.standing = True
        self.running = False
        self.jumping = False
        # lager en liste over alle bilder som skal vises når vi står stille
        self.standing_frames = [STANDING, STANDING2, STANDING3, STANDING4, STANDING5, STANDING6, STANDING7, STANDING8]

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()   # på starten av animate henter vi hvilken "tick" eller frame vi er på 1 tick er 1 FPS
 
        if self.standing:   # vis vi står stille, altså dette er animasjonen vi vil kjøre om vi status for player er "standing"         
            if now - self.last_update > 100:   # her sørger vi for at vi bytte bilde kun hver 350 tick, lavere tall animerer fortere
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
 
 
    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 5
            projectile = Ranged_attack(self.pos_x, self.pos_y, self.enemies, self.big_enemies, self.enemies_special)
            projectile.add(self.all_sprites)



    def big_attack(self):
        if self.attack_cooldown2 == 0:
            self.attack_cooldown2 = 500
            projectile = Big_attack(self.pos_x, self.pos_y, self.enemies, self.big_enemies, self.enemies_special)
            projectile.add(self.all_sprites)

 
    def update(self):
        self.animate() 
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y
        self.standing = True
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_cooldown2 > 0:
            self.attack_cooldown2 -= 1
        
        
        
        # player input
        keys = pg.key.get_pressed()
        if keys[pg.K_w]: # oppover
            self.pos_y -= self.speed
        if keys[pg.K_s]: # nedover
            self.pos_y += self.speed
        if keys[pg.K_a]: # venstre
            self.pos_x -= self.speed
        if keys[pg.K_d]: # høyre
            self.pos_x += self.speed 

        if self.pos_x < 0+self.width/2:
            self.pos_x = 0+self.width/2

        if self.pos_x > 2560-self.width:
            self.pos_x = 2560-self.width

        if self.pos_y < 0+self.height/2:
            self.pos_y = 0+self.height/2

        if self.pos_y > 1440-self.height:
            self.pos_y = 1440-self.height


        if keys[pg.K_SPACE]:
            self.attack()

        if keys[pg.K_f]:
            self.big_attack()



 
       
 
class Ranged_attack(pg.sprite.Sprite):
    def __init__(self, x, y, enemies, big_enemies, enemies_special): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = ranged_image
        self.rect = self.image.get_rect()
        self.enemies = enemies
        self.big_enemies = big_enemies
        self.enemies_special = enemies_special
        self.pos_x = x
        self.pos_y = y
        self.speed = 20
        self.damage = 10

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

    def update(self):
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        self.pos_x += self.speed #beveger til høyre

        if self.pos_x < 1:
            self.kill()

        hits = pg.sprite.spritecollide(self, self.enemies, False)
        if hits:
            print("hit")
            for enemy in hits:
                enemy.take_dmg(self.damage)


class Big_attack(pg.sprite.Sprite):
    def __init__(self, x, y, enemies, big_enemies, enemies_special): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = Big_ranged_image
        self.rect = self.image.get_rect()
        self.enemies = enemies
        self.big_enemies = big_enemies
        self.enemies_special = enemies_special
        self.pos_x = x
        self.pos_y = y
        self.speed = 20
        self.damage = 100

        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

    def update(self):
        self.rect.x = self.pos_x
        self.rect.y = self.pos_y

        self.pos_x += self.speed #beveger til høyre

        if self.pos_x < 1:
            self.kill()

        hits = pg.sprite.spritecollide(self, self.enemies, False)
        if hits:
            print("hit")
            for enemy in hits:
                enemy.take_dmg(self.damage)


class Enemy(pg.sprite.Sprite):
    def __init__(self): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.pos_x = random.randint(0,0)
        self.pos_y = random.randint(100,1440)
        self.speed = random.randint(-3,-3)
        self.damage = 10
        self.hp = 1000

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.pos_x -= self.speed

        if self.pos_x < 1:
            self.kill()


class Enemy2(pg.sprite.Sprite):
    def __init__(self): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = enemy2_image
        self.rect = self.image.get_rect()
        self.pos_x = random.randint(2200,2600)
        self.pos_y = random.randint(100,1440)
        self.speed = random.randint(6,6)
        self.damage = 10
        self.hp = 600

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.pos_x -= self.speed

        if self.pos_x < 1:
            self.kill()


class Enemy3(pg.sprite.Sprite):
    def __init__(self): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = enemy3_image
        self.rect = self.image.get_rect()
        self.pos_x = random.randint(2200,2600)
        self.pos_y = random.randint(100,1440)
        self.speed = random.randint(9,9)
        self.damage = 10
        self.hp = 400

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.pos_x -= self.speed

        if self.pos_x < 1:
            self.kill()


class Enemy4(pg.sprite.Sprite):
    def __init__(self): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = enemy4_image
        self.rect = self.image.get_rect()
        self.pos_x = random.randint(2200,2600)
        self.pos_y = random.randint(100,1440)
        self.speed = random.randint(12,12)
        self.damage = 10
        self.hp = 200

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.pos_x -= self.speed

        if self.pos_x < 1:
            self.kill()


class Big_enemy(pg.sprite.Sprite):
    def __init__(self): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = big_enemy_image
        self.rect = self.image.get_rect()
        self.pos_x = 2600
        self.pos_y = random.randint(700,700)
        self.speed = random.randint(1,1)
        self.damage = 50
        self.hp = 20000

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.pos_x -= self.speed

        if self.pos_x < 1:
            self.kill()


class Enemy_special(pg.sprite.Sprite):
    def __init__(self): # denne funksjonen kjører når vi lager player
        pg.sprite.Sprite.__init__(self)
        self.image = special_enemy_image
        self.rect = self.image.get_rect()
        self.pos_x = random.randint(2200,2600)
        self.pos_y = random.randint(100,1440)
        self.speed = random.randint(30,30)
        self.damage = 40
        self.hp = 10

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.rect.centerx = self.pos_x
        self.rect.centery = self.pos_y

        self.pos_x -= self.speed

        if self.pos_x < 1:
            self.kill()