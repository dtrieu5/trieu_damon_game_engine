#this file was created by: Damon Trieu

#imprt modules
import pygame as pg
from settings import *
# the asterix above means that it imports everything from the file
from random import randint
from sprites import *  
import sys

# TRANSPLANT THIS
from os import path


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
          self.map_data = []
          # 'r'     open for reading (default)
          # 'w'     open for writing, truncating the file first
           # 'x'     open for exclusive creation, failing if the file already exists
          # 'a'     open for writing, appending to the end of the file if it exists
          # 'b'     binary mode
           # 't'     text mode (default)
          # '+'     open a disk file for updating (reading and writing)
          # 'U'     universal newlines mode (deprecated)
          # below opens file for reading in text mode
          # with 
          '''
          The with statement is a context manager in Python. 
          It is used to ensure that a resource is properly closed or released 
           after it is used. This can help to prevent errors and leaks.
          '''
          with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
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
     def draw(self):
               self.screen.fill(BGCOLOR)
               self.draw_grid()
               self.all_sprites.draw(self.screen)
               pg.display.flip()

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

     def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player1 = Player (self, 1, 1)
        self.walls = pg.sprite.Group()
        self.all_sprites.add(self.player1)
          #    TRANSPLANT THIS
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)

     def move(self):
        pass


#create a new game
g = Game()
#run the game
# g.show_start_screen()
while True:
     g.new()
     g.run()
     # g.show_go_screen()