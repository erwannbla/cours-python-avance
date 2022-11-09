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

pg.init()
screen=pg.display.set_mode((args.width,args.height)) #on definit un ecran

clock=pg.time.Clock() #on definit une horloge
running=True  #condition pour que la boucle tourne

score=0
def damier(x,y,p):
        for i in range(x//p):
            for j in range(y//p):
                if (i+j)%2 !=0:
                    rect = pg.Rect(i*p, j*p, p, p)

                # appel à la méthode draw.rect()
                    color = [0, 0, 0] # couleur noire
                    pg.draw.rect(screen,color , rect)
                else:
                    rect = pg.Rect(i*p, j*p, p, p)

                # appel à la méthode draw.rect()
                    color = [255, 255, 255] # blanc
                    pg.draw.rect(screen,color,rect)

def snake(L):   #code de l'affichage du serpent
    for rectangle in L:  #L liste des tuples de positionnement des rectangles vert
        rectang=pg.Rect(rectangle[0]*args.dimpixel,rectangle[1]*args.dimpixel,args.dimpixel,args.dimpixel)
        pg.draw.rect(screen,(0,254,0),rectang)

def fruit(a,b):   #code de l'affichage du fruit
    rec=pg.Rect(a*args.dimpixel,b*args.dimpixel,args.dimpixel,args.dimpixel)
    pg.draw.rect(screen,(254,0,0),rec)

def scorejoueur(sc,l):  #prend en arguments score et liste
    Name=input('Nom du joueur:')
    l.append((sc,Name))
    print(l)
    for k in range(len(l)):
        f.write(f"{l[k][0]}, {l[k][1]}\n")
    
L= [(9, 13),
    (10, 13),
    (11, 13),
    (12,13)
]
direction=(0,1)
a=np.random.randint(0,args.width//args.dimpixel)
b=np.random.randint(0,args.height//args.dimpixel)

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
  
    damier(args.width,args.height,args.dimpixel)
    #pg.display.update()
    L.append((L[-1][0]+direction[0],L[-1][1]+direction[1])) #on fait avancer le snake en rajoutant un rectangle a sa liste et enlevant le dernier
    fruit(a,b)
    if L[-1]!=(a,b):  #si la tete ne rencontre pas le fruit
        del L[0]        #on supprime la derniere case ie le snake ne grandit pas
    else:
        a=np.random.randint(0,args.height//args.dimpixel)    #sinon on genere nouveau fruit
        b=np.random.randint(0,args.height//args.dimpixel)
        score=score+1
    
    #font = pg.font.Font(None, 20)
    #text = font.render(str(score),0, (255,255,255))
    #screen.blit(text, (20,20))
    
    snake(L)
    pg.display.update()

    if L[-1] in L[:-1]:     #si la tete du snake touche son corps on perd
        running=False
        print('game over')
    elif L[-1][0]<0 or L[-1][0]>= (args.width//args.dimpixel):
        running=False
        print('game over')
    elif L[-1][1]<0 or L[-1][1]>= (args.height//args.dimpixel):
        running=False
        print('game over')
    
pg.quit()
l=[]
if not(os.path.exists('highscore.txt')):
    with open('highscore.txt','w') as f:
        scorejoueur(score,l)
else:
    with open('highscore.txt','r') as f:
        
        for line in f:
            if line=='\n':
                pass
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