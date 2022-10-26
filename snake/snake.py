from random import randint
import pygame as pg
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
#parser.add_argument('integers', metavar='N', type=int, nargs='+',
 #                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
 #                   const=sum, default=max,
 #                   help='sum the integers (default: find the max)')
parser.add_argument('--height', type=int, help='height', default=600)
parser.add_argument('--width', type=int, help='width', default=600)
parser.add_argument('--heightpixel', type=int, help='heightp', default=20)
parser.add_argument('--widthpixel', type=int, help='widthp', default=20)
args = parser.parse_args()
print(args) #affiche dans le bash les arguments


pg.init()
screen=pg.display.set_mode((args.width,args.height))

clock=pg.time.Clock()
running=True
while running:

    clock.tick(1) # regarde le temps entre 2 boucles et attend 1s sinon bloque
    for event in pg.event.get():  #renvoie none si pas event
            if event.type == pg.QUIT:
                running=False
        # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
            # si la touche est "Q" on veut quitter le programme
                if event.key == pg.K_q:
                    running=False

    random_color=(randint(0,255),randint(0,255),randint(0,255))
    screen.fill((255,255,255))
    pg.display.update()
    
    for i in range(args.height//args.heightpixel):
        for j in range(args.width//args.widthpixel):
            if (i+j)%2 ==0:
                rect = pg.Rect(i*args.heightpixel, j*args.widthpixel, args.widthpixel, args.heightpixel)

                # appel à la méthode draw.rect()
                color = (0, 0, 0) # couleur blanche
                pg.draw.rect(screen,color , rect)
    pg.display.update()

    snake = [
    (10, 15),
    (11, 15),
    (12, 15),
]

    for rectangle in snake:
        

