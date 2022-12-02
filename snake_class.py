from random import randint
import numpy as np
import pygame as pg
import argparse
import os 
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

score=0
pg.init()
screen=pg.display.set_mode((args.width,args.height)) #on definit un ecran

clock=pg.time.Clock() #on definit une horloge
running=True  #condition pour que la boucle tourne


class damier:

    def __init__(self, height, width, pixel):
        self.height = height
        self.width = width
        self.pixel = pixel

    def affiche_damier(self):
        for i in range(self.height//self.pixel):
            for j in range(self.width//self.pixel):
                if (i+j)%2 !=0:
                    rect = pg.Rect(i*self.pixel, j*self.pixel, self.pixel, self.pixel)

                # appel à la méthode draw.rect()
                    color = [0, 0, 0] # couleur noire
                    pg.draw.rect(screen, color, rect)
                else:
                    rect = pg.Rect(i*self.pixel, j*self.pixel, self.pixel, self.pixel)

                # appel à la méthode draw.rect()
                    color = [255, 255, 255] # blanc
                    pg.draw.rect(screen,color,rect)
class snake:
    def __init__(self, liste_snake, directi):
        self.liste_snake = liste_snake
        self.direction = directi
        
    def affiche_snake(self):   #code de l'affichage du serpent
        #lis_snake = self.liste_snake
        for rectangle in self.liste_snake:  #liste_snake = liste des tuples de positionnement des rectangles vert
            rectang=pg.Rect(rectangle[0]*damier.pixel,rectangle[1]*damier.pixel,damier.pixel,damier.pixel)
            pg.draw.rect(screen,(0,254,0),rectang)
        
    def avance_snake(self):
        self.liste_snake.append((self.liste_snake[-1][0]+self.direction[0],self.liste_snake[-1][1]+self.direction[1])) #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
        return self.liste_snake
       
    def manger_fruit(self):    
        if self.liste_snake[-1]!=fruit.position:  #si la tete ne rencontre pas le fruit
            del self.liste_snake[0] 
        else:
            fruit.position=fruit(fruit.position).position_fruit()
            score=score+1

            #on met ensuit fruit.affiche_fruit()?

    def mort_snake(self):   
        if self.liste_snake[-1] in self.liste_snake[:-1]:     #si la tete du snake touche son corps on perd
            running=False
            print('game over')
        elif self.liste_snake[-1][0]<0 or self.liste_snake[-1][0]>= (damier.width//damier.pixel):
            running=False
            print('game over')
        elif self.liste_snake[-1][1]<0 or self.liste_snake[-1][1]>= (damier.height//damier.pixel):
            running=False
            print('game over')

class fruit:
    def __init__(self, position): #position est un couple
        self.position = position
        
    def position_fruit():
        a=np.random.randint(0,damier.height//damier.pixel)    #sinon on genere nouveau fruit
        b=np.random.randint(0,damier.height//damier.pixel)
        return (a,b)

    def affiche_fruit(self):   #code de l'affichage du fruit
        rec=pg.Rect(self.position[0]*damier.pixel,self.position[1]*damier.pixel,damier.pixel,damier.pixel)
        pg.draw.rect(screen,(254,0,0),rec)

def scorejoueur(sc,l):  #prend en arguments score et liste
    Name=input('Nom du joueur:')
    l.append((sc,Name))
    l=sorted(l)
    for k in range(len(l)):
        f.write(f"{l[k][0]}, {l[k][1]}\n")

liste_snake_init= [(9, 13),
    (10, 13),
    (11, 13),
    (12,13)
]
direction=(0,1)

fruit.position=fruit.position_fruit()
while running:

    clock.tick(5) # regarde le temps entre 2 boucles et attend 1s sinon bloque
    for event in pg.event.get():  #renvoie none si pas event
            if event.type == pg.QUIT:
                running=False
        # un type de pg.KEYDOWN signifie que l'on a appuye une touche du clavier
            elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
                if event.key == pg.K_q:
                    running=False
                if event.key == pg.K_UP:
                    direction = (0,-1)
                if event.key == pg.K_DOWN:
                    direction=(0,1)
                if event.key == pg.K_LEFT:
                    direction=(-1,0)
                if event.key == pg.K_RIGHT:
                    direction=(1,0)

   # random_color=(randint(0,255),randint(0,255),randint(0,255))
    #screen.fill((255,255,255))
  
    damier(args.width,args.height,args.dimpixel).affiche_damier() 
    #pg.display.update()
    L=snake(liste_snake_init,direction).avance_snake()  #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
    fruit(fruit.position_fruit).affiche_fruit()
    snake(liste_snake_init,direction).manger_fruit()  #si la tete ne rencontre pas le fruit
                #on supprime la derniere case ie le snake ne grandit pas
    
    
    #font = pg.font.Font(None, 20)
    #text = font.render(str(score),0, (255,255,255))
    #screen.blit(text, (20,20))
    
    snake(L,direction).affiche_snake()
    pg.display.update()
    snake(L,direction).mort_snake()
    
pg.quit()
l=[]
if not(os.path.exists('highscore.txt')):
    with open('highscore.txt','w') as f:
        scorejoueur(score,l)
else:
    with open('highscore.txt','r') as f:
        
        for line in f:
            if line=='\n':
                del line
            else:
                s,nom=int(line.split(',')[0]), line.split(',')[1]
                l.append((s,nom))
        if len(l)<5:
            
            with open('highscore.txt','w') as f:
                scorejoueur(score,l)
        else:
            l=sorted(l)
            if score>l[0][0]:
                l.pop(0)
                with open('highscore.txt','w') as f:    
                    scorejoueur(score,l)
system("cat highscore.txt")