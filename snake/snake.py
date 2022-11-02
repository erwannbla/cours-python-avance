from random import randint
import numpy as np
import pygame as pg
import argparse
import pathlib 

parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
 #                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
 #                   const=sum, default=max,
 #                   help='sum the integers (default: find the max)')
parser.add_argument('--height', type=int, help='height', default=400)
parser.add_argument('--width', type=int, help='width', default=400)
parser.add_argument('--heightpixel', type=int, help='heightp', default=20)
parser.add_argument('--widthpixel', type=int, help='widthp', default=20)
args = parser.parse_args()
print(args) #affiche dans le bash les arguments

pg.init()
screen=pg.display.set_mode((args.width,args.height))

clock=pg.time.Clock()
running=True

score=0
def snake(L):
    for rectangle in L:  #L liste des tuples de positionnement des rectangles vert
        rectang=pg.Rect(rectangle[0]*args.widthpixel,rectangle[1]*args.heightpixel,args.widthpixel,args.heightpixel)
        pg.draw.rect(screen,(0,254,0),rectang)

def fruit(a,b):
    rec=pg.Rect(a*args.widthpixel,b*args.heightpixel,args.widthpixel,args.heightpixel)
    pg.draw.rect(screen,(254,0,0),rec)
    
L= [(9, 13),
    (10, 13),
    (11, 13),
    (12,13)
]
direction=(0,1)
a=np.random.randint(0,args.width//args.widthpixel)
b=np.random.randint(args.height//args.heightpixel)

while running:

    clock.tick(5) # regarde le temps entre 2 boucles et attend 1s sinon bloque
    for event in pg.event.get():  #renvoie none si pas event
            if event.type == pg.QUIT:
                running=False
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
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
    screen.fill((255,255,255))
    pg.display.update()

    
    for i in range(args.width//args.widthpixel):
        for j in range(args.height//args.heightpixel):
            if (i+j)%2 ==0:
                rect = pg.Rect(i*args.heightpixel, j*args.widthpixel, args.widthpixel, args.heightpixel)

                # appel à la méthode draw.rect()
                color = (0, 0, 0) # couleur blanche
                pg.draw.rect(screen,color , rect)
    
    L.append((L[-1][0]+direction[0],L[-1][1]+direction[1]))
    fruit(a,b)
    if L[-1]!=(a,b):
        del L[0]
    else:
        a=np.random.randint(0,args.height//args.heightpixel)
        b=np.random.randint(0,args.height//args.heightpixel)
        score=score+1
    
    font = pg.font.Font(None, 20)
    text = font.render(str(score),0, (255,255,255))
    screen.blit(text, (20,20))
    
    snake(L)
    pg.display.update()

    if L[-1] in L[:-1]:
        running=False
        print('game over')
    elif L[-1][0]<0 or L[-1][0]>= (args.width//args.widthpixel):
        running=False
        print('game over')
    elif L[-1][1]<0 or L[-1][1]>= (args.height//args.heightpixel):
        running=False
        print('game over')
    
pg.quit()
if not(os.path.exists(highscore.txt)):
    with open('highscore.txt','w') as f:
        Name=input('Nom du joueur:')
        f.write((Name, score)/n)
else:
    with open('highscore.txt','r') as f:
        for count, line in enumerate(fp):
            pass
        if count+1<5:
            Name=input('Nom du joueur:')
            print(Name, score)
        else:
            with open('highscore.txt','w') as fd:
