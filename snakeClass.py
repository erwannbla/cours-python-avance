from random import randint
import numpy as np
import pygame as pg
import argparse
import os 
from pathlib import Path
from os import system
import re

parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
 #                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
 #                   const=sum, default=max,
 #                   help='sum the integers (default: find the max)')
parser.add_argument('--height', type=int, help='height', default=400) #le joueur definit largeur et longueur de sa fenetre de jeu +pixel
parser.add_argument('--width', type=int, help='width', default=400)
parser.add_argument('--dimpixel', type=int, help='dimp', default=20)
parser.add_argument('--fruitcolor', type=str, help='fruitcolot', default='#FF0000')
parser.add_argument('--snakecolor', type=str, help='snakecolot', default='#00FF00')

args = parser.parse_args()

print(args) #affiche dans le bash les arguments
re1= r"^#[a-f0-9A-F]{6}$"
if not(re.search(re1,args.fruitcolor)):     #test si format couleur compatible
    print('couleur fruit pas compatible hexadecimal')
    exit()
elif not(re.search(re1,args.snakecolor)):
    print('couleur snake pas compatible hexadecimal')
    exit()
else:
    pass

#test si arguments fenetres bien divisibles
if (args.height % args.dimpixel !=0) or (args.width % args.dimpixel !=0) :
    print('erreur:largeur pixel nest pas un diviseur de la largeur de la fenetre')
    exit()
else:
    pass


pg.init()

class Game:
    def __init__(self):
        self._running=True
        self._direction =(1,0)
    
    def test(self):
        return self._running
    def Getdirection(self):
        return self._direction
    
    def clock(self): #defines a clock for the fps of the game
        return pg.time.Clock()


    def moves(self):
        for event in pg.event.get():  #renvoie none si pas event
            if event.type == pg.QUIT:
                self._running=False
        # un type de pg.KEYDOWN signifie que l'on a appuye une touche du clavier
            elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
                if event.key == pg.K_q:
                    self._running=False
                if event.key == pg.K_UP:
                    self._direction = (0,-1)
                if event.key == pg.K_DOWN:
                    self._direction=(0,1)
                if event.key == pg.K_LEFT:
                    self._direction=(-1,0)
                if event.key == pg.K_RIGHT:
                    self._direction=(1,0)



class Damier: #on definit l'objet damier

    def __init__(self, height=args.height, width=args.width, 
    pixel=args.dimpixel, color_fruit=args.fruitcolor, color_snake=args.snakecolor):
        self._height = height
        self._width = width
        self._pixel = pixel
        self._color_fruit=color_fruit
        self._color_snake=color_snake
    
    def getheight(self):
        return self._height
    
    def getpixel(self):
        return self._pixel
    
    def getwidth(self):
        return self._width
    
    def screen(self):       #creates screen with pygame
        return pg.display.set_mode((self._width,self._height))

    def affiche_damier(self):       #draw a board painting one case in black and another in white
        for i in range(self._height//self._pixel):
            for j in range(self._width//self._pixel):
                if (i+j)%2 !=0:
                    rect = pg.Rect(i*self._pixel, j*self._pixel, self._pixel, self._pixel)

                # appel à la méthode draw.rect()
                    color = [0, 0, 0] # couleur noire
                    pg.draw.rect(screen, color, rect)
                else:
                    rect = pg.Rect(i*self._pixel, j*self._pixel, self._pixel, self._pixel)

                # appel à la méthode draw.rect()
                    color = [255, 255, 255] # blanc
                    pg.draw.rect(screen,color,rect)
    
    def affiche_snake(self, list_snake):
        '''
        draws a snake from a given liste with the positions
        '''
        for rectangle in list_snake:  #liste_snake = liste des tuples de positionnement des rectangles vert
            rectang=pg.Rect(rectangle[0]*self._pixel,rectangle[1]*self._pixel,self._pixel,self._pixel)
            pg.draw.rect(screen,self._color_snake,rectang)
    
    def position_fruit(self):
        '''
        generates new position for the fruit
        '''
        a=np.random.randint(0,self._height//self._pixel)
        b=np.random.randint(0,self._width//self._pixel)
        return (a,b)
    
    def affiche_fruit(self, pos_fruit):   #draws the fruit
        rec=pg.Rect(pos_fruit[0]*self._pixel,pos_fruit[1]*self._pixel,self._pixel,self._pixel)
        pg.draw.rect(screen,self._color_fruit,rec)


class Snake:            #class avec majuscule, fonction avec minuscule
    #syntaxe java : mots separes par majuscule
    #syntaxe C++ mots separes par _
    def __init__(self, liste_snake=[(9, 13),(10, 13),(11, 13),(12,13)], direction=(1,0)):
        self._liste_snake = liste_snake
        self._direction = direction

    def getliste_snake(self):
        return self._liste_snake
    
    def getdirection(self):
        return self._direction
    
    def NewDirection(self,d):
        self._direction=d
        
    def avance_snake(self):
        '''
        moves the snake in the current direction by adding its values to the
        snake list
        '''
        self._liste_snake.append((self._liste_snake[-1][0]+self._direction[0],self._liste_snake[-1][1]+self._direction[1])) #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
        return self._liste_snake

    def manger_fruit(self,fru,object,sco):    
        if self._liste_snake[-1]!=fru.getposition():  #si la tete ne rencontre pas le fruit
            del self._liste_snake[0]    #on enleve la derniere position de la liste
        else:
            #sinon nouveau fruit et score +1
            fru._position=object.position_fruit()
            sco._score+=1

    def mort_snake(self,object):
        if self._liste_snake[-1] in self._liste_snake[:-1]:     
            #si la tete du snake touche son corps on perd
            print('game over')
            object._running= False  #ends the while True
        
        elif self._liste_snake[-1][0]<0 or self._liste_snake[-1][0]>= (damier.getwidth()//damier.getpixel()):
            #dies if touches the walls
            print('game over')
            object._running= False
        elif self._liste_snake[-1][1]<0 or self._liste_snake[-1][1]>= (damier.getheight()//damier.getpixel()):
            
            print('game over')
            object._running= False

class Fruit:
    def __init__(self, position=Damier().position_fruit()): #position est un couple aleatoire
        self._position = position
    
    def getposition(self):
        return self._position

class Score:
    def __init__(self,score=0,liste_score=[]):
        self._score=score
        self._liste_score=liste_score

    def GetScore(self):
        return self._score
    
    def displayScore(self):  #display the current score while playing thank to pygame function
        pg.display.set_caption(f"Score:{self._score}")
        
    def scorejoueur(self,scor,list): 
        ''' 
        prend en arguments nouveau score et liste de scores
        pour ecrire sur le fichier
        '''
        Name=input('Nom du joueur:')
        list.append((scor,Name))
        
        with open('highscore.txt', 'w') as f :
            for k in range(len(list)):
                f.write(f"{list[k][0]}, {list[k][1]}\n")
        
    def write_score(self,obj):
        '''
        check if highscore.txt exist and keeps top 5 score
        '''
        if not(os.path.exists('highscore.txt')):
            Name=input('Nom du joueur:')
            with open('highscore.txt','w') as f:        #opens the files to write
                f.write(f"{obj.GetScore()}, {Name}\n")
        else:
            with open('highscore.txt','r') as f:        #opens to read and save the data
        
                for line in f:
                    if line=='\n':
                        del line
                    else:
                        s,nom=int(line.split(',')[0]), line.split(',')[1]
                        self._liste_score.append((s,nom))
                print(self._liste_score)
                if len(self._liste_score)<5:
                    #if less than 5 top scores we add the current one
                    Score().scorejoueur(obj.GetScore(),self._liste_score)
                else:
                    #otherwise tests if new top 5 score or not
                    l=self._liste_score
                    l=sorted(l)
                    if self._score > l[0][0]:
                        l.pop(0)
                        print('New top 5')
                        Score().scorejoueur(obj.GetScore(),l)
                    else:
                        print('Not new top 5')

#definition of the objects
snake=Snake()
fruit=Fruit()
game=Game()
score=Score()
damier=Damier()

screen=damier.screen()
clock=game.clock()

while game.test(): #tant qu'on a pas de mort du serpent

    clock.tick(5) # regarde le temps entre 2 boucles et attend 1/5s sinon bloque
  
    damier.affiche_damier() 
    score.displayScore()
  
    game.moves()
    snake.NewDirection(game.Getdirection())
    snake.avance_snake()  #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
    damier.affiche_fruit(fruit.getposition())
    snake.manger_fruit(fruit,damier,score)
    
    damier.affiche_snake(snake.getliste_snake())
    pg.display.update()
    snake.mort_snake(game)
    
pg.quit()
score.write_score(score)

system("cat highscore.txt")

if __name__=='__main__':
    print('launched from the original file')
else:
    print('lauched with another file')
