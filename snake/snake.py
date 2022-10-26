from random import randint
import pygame as pg
pg.init()
screen=pg.display.set_mode((400,300))

clock=pg.time.Clock()
while True:

    clock.tick(1) # regarde le temps entre 2 boucles et attend 1s sinon bloque

    for event in pg.event.get():  #renvoie none si pas event
        pass

    random_color=(randint(0,255),randint(0,255),randint(0,255))
    screen.fill(random_color)
    pg.display.update()