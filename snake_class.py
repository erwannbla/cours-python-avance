from random import randint
import numpy as np
import pygame as pg
import argparse
import os 
from pathlib import Path
from os import system

parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
 #                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
 #                   const=sum, default=max,
 #                   help='sum the integers (default: find the max)')
parser.add_argument('--height', type=int, help='height', default=400) #le joueur definit largeur et longueur de sa fenetre de jeu +pixel
parser.add_argument('--width', type=int, help='width', default=400)
parser.add_argument('--dimpixel', type=int, help='dimp', default=20)

args = parser.parse_args()
print(args) #affiche dans le bash les arguments

if (args.height % args.dimpixel !=0) or (args.width % args.dimpixel !=0) :
    print('erreur:largeur pixel nest pas un diviseur de la largeur de la fenetre')
    exit()
else:
    pass


pg.init()
screen=pg.display.set_mode((args.width,args.height)) #on definit un ecran

clock=pg.time.Clock() #on definit une horloge
  #condition pour que la boucle tourne

class Game:
    def __init__(self):
        self._running=True
        self._direction =(1,0)
    
    def test(self):
        return self._running
    def Getdirection(self):
        return self._direction


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



class Damier:

    def __init__(self, height=args.height, width=args.width, pixel=args.dimpixel):
        self._height = height
        self._width = width
        self._pixel = pixel
    
    def getheight(self):
        return self._height
    
    def getpixel(self):
        return self._pixel
    
    def getwidth(self):
        return self._width

    def affiche_damier(self):
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
    
    def affiche_snake(self, list_snake):   #code de l'affichage du serpent
        #lis_snake = self.liste_snake
        for rectangle in list_snake:  #liste_snake = liste des tuples de positionnement des rectangles vert
            rectang=pg.Rect(rectangle[0]*self._pixel,rectangle[1]*self._pixel,self._pixel,self._pixel)
            pg.draw.rect(screen,(0,254,0),rectang)
    
    def position_fruit(self):
        a=np.random.randint(0,self._height//self._pixel)    #sinon on genere nouveau fruit
        b=np.random.randint(0,self._width//self._pixel)
        return (a,b)
    
    def affiche_fruit(self, pos_fruit):   #code de l'affichage du fruit
        rec=pg.Rect(pos_fruit[0]*self._pixel,pos_fruit[1]*self._pixel,self._pixel,self._pixel)
        pg.draw.rect(screen,(254,0,0),rec)


class Snake:            #class avec majuscule, fonction avec minuscule
    #syntaxe java mots separes par majuscule
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
        self._liste_snake.append((self._liste_snake[-1][0]+self._direction[0],self._liste_snake[-1][1]+self._direction[1])) #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
        return self._liste_snake

    def manger_fruit(self,fru,object,sco):    
        if self._liste_snake[-1]!=fru.getposition():  #si la tete ne rencontre pas le fruit
            del self._liste_snake[0] 
        else:
            fru._position=object.position_fruit()
            sco._score+=1

    def mort_snake(self,object):   
        if self._liste_snake[-1] in self._liste_snake[:-1]:     #si la tete du snake touche son corps on perd
            
            print('game over')
            object._running= False
        elif self._liste_snake[-1][0]<0 or self._liste_snake[-1][0]>= (damier.getwidth()//damier.getpixel()):
            
            print('game over')
            object._running= False
        elif self._liste_snake[-1][1]<0 or self._liste_snake[-1][1]>= (damier.getheight()//damier.getpixel()):
            
            print('game over')
            object._running= False

class Fruit:
    def __init__(self, position=Damier().position_fruit()): #position est un couple
        self._position = position
    
    def getposition(self):
        return self._position

class Score:
    def __init__(self,score=0,liste_score=[]):
        self._score=score
        self._liste_score=liste_score

    def GetScore(self):
        return self._score
    
    def displayScore(self):
        pg.display.set_caption(f"Score:{self._score}")

   # def raise_score(self):
   #     self._score=self._score + 1
        
    def scorejoueur(self):  #prend en arguments score et liste
        Name=input('Nom du joueur:')
        self._liste_score.append((Name,self._score))
        self._liste_score=sorted(self._liste_score[1])
        with open('highscore.txt', 'w') as f :
            for k in range(len(self._liste_score)):
                f.write(f"{self._liste_score[k][0]}, {self._liste_score[k][1]}\n")
        
    def write_score(self):
        if not(os.path.exists('highscore.txt')):
            with open('highscore.txt','w') as f:
                Score().scorejoueur()
        else:
            with open('highscore.txt','r') as f:
        
                for line in f:
                    if line=='\n':
                        del line
                    else:
                        nom,s=int(line.split(',')[0]), line.split(',')[1]
                        self._liste_score.append((nom,s))
                if len(self._liste_score)<5:
            
                    Score().scorejoueur()
                else:
                    self._liste_score=sorted(self._liste_score)
                    if self._score > self._liste_score[0][1]:
                        self._liste_score.pop(0)
                            
                        Score().scorejoueur()

snake=Snake()
fruit=Fruit()
game=Game()
score=Score()
damier=Damier()

while game.test():

    clock.tick(5) # regarde le temps entre 2 boucles et attend 1s sinon bloque
  
    damier.affiche_damier() 
    score.displayScore()
    #pg.display.update()
    game.moves()
    snake.NewDirection(game.Getdirection())
    snake.avance_snake()  #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
    damier.affiche_fruit(fruit.getposition())
    snake.manger_fruit(fruit,damier,score)  #si la tete ne rencontre pas le fruit
                #on supprime la derniere case ie le snake ne grandit pas
    
    
    damier.affiche_snake(snake.getliste_snake())
    pg.display.update()
    snake.mort_snake(game)
    
pg.quit()
score.write_score()

system("cat highscore.txt")