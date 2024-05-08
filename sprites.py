# This file was created by: Damon Trieu
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
# allows us to use pygame and imports all settings from settings

# inherit from subclass of pg.sprite
class Player(pg.sprite.Sprite):
    # initialize the player class
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # fills self image with color (GREEN)
        # self.image.fill(GREEN)
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.status = ""
        self.hitpoints = 100
        self.cooling = False
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_k]:
            print('k')
            BoomBoom(self.game, self.x, self.y + TILESIZE * 2)
        if keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_DOWN]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, 0, -10)
        if keys[pg.K_UP]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, 0, 10)
        if keys[pg.K_LEFT]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, -10, 0)
        if keys[pg.K_RIGHT]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, 10, 0)
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071


    # def move(self, dx=0 , dy=0):
    #     self.x += dx
    #     self. y +=dy


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                self.speed += 80
                self.game.cooldown.cd = 5
                self.cooling = True
            # if str(hits[0].__class__.__name__) == "Mob":
            #     # print(hits[0].__class__.__name__)
            #     # print("Collided with mob")
            #     # self.hitpoints -= 1
            #     if self.status == "Invincible":
            #         print("you can't hurt me")

    # def collide_with_walls(self, dir):
    #     if dir == 'x':
    #         hits=pg.sprite.spritecollide(self. self.game.walls, False)
    #         if hits:
    #             if self.vx > 0:
    #                 self.x = hits[0].rect.left - self.rect.width
    #             if self.vx < 0:
    #                 self.x = hits[0].rect.right
    #             self.vx = 0
    #             self.rect.x = self.x
    #     if dir == 'y':
    #         hits=pg.sprite.spritecollide(self. self.game.walls, False)
    #         if hits:
    #             if self.vy > 0:
    #                 self.y = hits[0].rect.top - self.rect.height
    #             if self.vy < 0:
    #                 self.y = hits[0].rect.bottom
    #             self.vy = 0
    #             self.rect.y = self.y


    def update(self):
        self.get_keys()
        self.x +=self.vx * self.game.dt
        self.y +=self.vy * self.game.dt
        self.rect.x=self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y=self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
        #     self.moneybag += 1
        # coin_hits = pg.sprite.spritecollide(self, self.game.coins, True)
    
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        # init superclass
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x *TILESIZE
        self.rect.y = y *TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(LIGHTBLUE)
        self.image = game.Powerup_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player1.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player1.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player1.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player1.rect.y:
            self.vy = -100
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')

class SuperMob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.supermobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(RED)
        self.image = game.SuperMob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 60
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player1.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player1.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player1.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player1.rect.y:
            self.vy = -100
        self.rect.x = self.x
        # self.collide_with_walls('x')
        self.rect.y = self.y
        # self.collide_with_walls('y')

class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y, xspeed, yspeed):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        # make bullets orange
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        # initiate speed of bullets
        self.xspeed = xspeed
        self.yspeed = yspeed
        print("I created a pew pew...")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        # if hits:
        #     if str(hits[0].__class__.__name__) == "Coin":
        #         self.moneybag += 1
    def update(self):
        # makes projectiles kill coins
        self.collide_with_group(self.game.coins, True)
        # makes projectiles kill powerups
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, True)
        self.rect.x += self.xspeed
        self.rect.y -= self.yspeed
        # pass

class BoomBoom(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boom_booms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE // 2, TILESIZE // 2))  # Larger projectile size
        self.image.fill(YELLOW)  # Set color for larger projectiles (e.g., yellow)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 3  # Slower speed for larger projectiles
        self.fire_delay = 10  # Slower fire rate (adjust as needed)
        self.last_fire_time = pg.time.get_ticks()

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        for hit in hits:
            # Handle collision logic with specific group (e.g., coins, power-ups, mobs)
            pass

    def update(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_fire_time > self.fire_delay:
            self.last_fire_time = current_time
            self.rect.y -= self.speed
            self.collide_with_group(self.game.coins, True)
            self.collide_with_group(self.game.power_ups, True)
            self.collide_with_group(self.game.mobs, True)
        
