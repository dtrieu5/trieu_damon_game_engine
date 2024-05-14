# This file was created by: Damon Trieu
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from pygame.sprite import Group
from settings import *
# allows us to use pygame and imports all settings from settings
# copied from chatgpt
class Health(pg.sprite.Sprite):
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health < 0:
            self.current_health = 0

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def is_alive(self):
        return self.current_health > 0


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
        self.health = Health(max_health=10)
        self.moneybag = 0
        self.speed = 300
        self.status = ""
        self.hitpoints = 100
        self.cooling = False

        def update(self):
        # Handle movement and other updates

        # Collision with mobs
            hits = pg.sprite.spritecollide(self, self.game.mobs, False)
            for mob in hits:
            # Reduce player health when hit by a mob
                self.health.take_damage(1)  # Adjust damage amount as needed
            if not self.health.is_alive():
                # Player is dead, handle game over logic here
                self.game_over()
            def game_over(self):
        # Reset the game or show game over screen
                self.game.show_game_over_screen()  # Implement this method in your Game class
            
        def collide_with_mobs(self):
        # Check for collisions with mobs
            hits = pg.sprite.spritecollide(self, self.game.mobs, False)
            for mob in hits:
            # Reduce player health when hit by a mob
                self.health.take_damage(1)
                if not self.health.is_alive():
                    self.game_over()
    
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
            PewPew(self.game, self.x, self.y, 0, -10, 300)
        if keys[pg.K_UP]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, 0, 10, 300)
        if keys[pg.K_LEFT]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, -10, 0, 300)
        if keys[pg.K_RIGHT]:
            print("trying to shoot ...")
            PewPew(self.game, self.x, self.y, 10, 0, 300)
        # if keys [pg.K_i]:
        #     print("trying to shoot ...")
        #     BoomBoom(self.game, self.x, self.y, 0,10)
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
            if str(hits[0].__class__.__name__) == "Mob":
                self.hitpoints -= 1
                hits[0].health -= 1
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Supermob":
                self.hitpoints -= 1
                hits[0].health -= 1
                if self.status == "Invincible":
                    print("you can't hurt me")
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
    def __init__(self, game, x, y, health = 15):
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
        self.health = health

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
    def take_damage(self, damage):
        self.health = damage
        if self.health <=0:
            self.kill()

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
    def __init__(self, game, x, y, xspeed, yspeed, max_range):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        # make bullets orange
        self.image = game.pewpew_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        # initiate speed of bullets
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.max_range_pixels = max_range
        self.distance_traveled = 0
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
        self.distance_traveled += abs(self.xspeed) + abs(self.yspeed)
        # pass
        if self.distance_traveled > self.max_range_pixels:
            self.kill()
        hits = pg.sprite.spritecollide(self, self.game.mobs, True)
        for mob in hits:
            mob.take_damage(1)  # Reduce mob's health by 1 when hit by pew pew
            if mob.health <= 0:
                self.game.score += 1  # Increase score when mob is defeated

        # Destroy pew pew when it goes off-screen
        if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
            self.kill()  # Remove pew pew from sprite groups

class BoomBoom(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.boom_booms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.boomboom_img
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = 3  # Slower speed for larger projectiles
        self.fire_delay = 0.2  # Slower fire rate (adjust as needed)
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
            self.collide_with_group(self.game.supermobs, True)
    
        
