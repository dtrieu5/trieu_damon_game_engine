#this file was created by: Damon Trieu
# 3 goals to add
     # moving enemies
     # projectiles to shoot enemies
     # more maps/different maps
# one main goal
     # make the game more difficult/add boss fight
     

#imprt modules
import pygame as pg
from settings import *
# the asterix above means that it imports everything from the file
from random import randint
from sprites import *  
import sys
from os import path

# this is to test github
#creating game blueprint
class Game:
    #Initializeraaaa
     def __init__(self):
        #Initializes pygame
        pg.init()
        # Settings
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        #setting up pygame clock
        self.clock = pg.time.Clock()
        self.load_data()
  
    
     def load_data(self):
          game_folder = path.dirname(__file__)
          self.img_folder = path.join(game_folder, 'images')

          self.player_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'invincible.png')).convert_alpha(), (60, 60))
          self.mob_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'mario-skeleton.png')).convert_alpha(), (55, 55))
          self.coin_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'coin.png')).convert_alpha(), (45, 45))
          self.SuperMob_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'superbowser.png')).convert_alpha(), (85, 85))
          self.Powerup_img = pg.transform.scale(pg.image.load(path.join(self.img_folder, 'burger.png')).convert_alpha(), (45, 45))
          self.map_data = []

          with open(path.join(game_folder, 'map.txt'), 'r') as f:
               for line in f:
                    self.map_data.append(line)

    # runs our game
     def run(self):
          #game loop -- keep running until we want to stop
          self.playing = True
          while self.playing:
               self.dt = self.clock.tick(FPS) / 1000
               self.events()
               self.update()
               self.draw()

     def quit(self):
          pg.quit()
          sys.exit()

     def update(self):
          self.all_sprites.update() 

     def draw_grid(self):
          for x in range(0, WIDTH, TILESIZE):
               pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
          for y in range(0, HEIGHT, TILESIZE):
               pg.draw.line(self.screen, LIGHTGREY, (0,y), (WIDTH, y)) 
     def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)

        

     def draw(self):
               self.screen.fill(BGCOLOR)
               self.draw_grid()
               self.all_sprites.draw(self.screen)
               pg.display.flip()
               # self.draw_health_bar(self.screen, self.player1.rect.x, self.player1.rect.y-8, self.player1.hitpoints)
               # for m in self.mobs:
               #      self.draw_health_bar(self.screen, m.rect.x, m.rect.y-8, m.hitpoints*20)
               # pg.display.flip()
          
     
     
     def events(self):
          for event in pg.event.get():
               if event.type == pg.QUIT:
                    self.quit()
               # if event.type == pg.KEYDOWN:
               #      # moves player to the left 1
               #      if event.key == pg.K_LEFT:
               #           self.player1.move(dx=-1)
               #      # moves player to the right 1
               #      if event.key == pg.K_RIGHT:
               #           self.player1.move(dx=1)
               #      # moves player up 1
               #      if event.key == pg.K_UP:
               #           self.player1.move(dy=-1)
               #      # moves player down 1
               #      if event.key == pg.K_DOWN:
               #           self.player1.move(dy=1)
     def show_start_screen(self):
          self.screen.fill(BGCOLOR)
          self.draw_text(self.screen, "this is the start screen", 24, WHITE, WIDTH/2 - 32, 2)
          pg.display.flip()
          self.wait_for_key()

     def wait_for_key(self):
               waiting = True
               while waiting:
                    self.clock.tick(FPS)
                    for event in pg.event.get():
                         if event.type == pg.QUIT:
                              waiting = False
                              self.quit()
                         if event.type == pg.KEYUP:
                              waiting = False






     def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player1 = Player (self, 1, 1)
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.supermobs = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.chest = pg.sprite.Group()
        self.boom_booms = pg.sprite.Group()
        self.all_sprites.add(self.player1)
          #    TRANSPLANT THIS
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
               print(col)
               if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
               if tile == 'P':
                    self.player1 = Player(self, col, row)
               if tile == 'C':
                    Coin(self,col, row) 
               if tile == 'U':
                    Powerup(self, col, row)
               if tile == 'M':
                    Mob(self, col, row)
               if tile == 'S':
                    SuperMob(self,col,row)


     def move(self):
        pass


#create a new game
g = Game()
#run the game
g.show_start_screen()
# g.show_start_screen()
while True:
     g.new()
     g.run()
     # g.show_go_screen()