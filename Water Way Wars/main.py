import pygame
from pygame.locals import *
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from Scripts.eventLoop import eventLoop
from Scripts.ui import Text, Button
from Scripts.Objects import Submarine, Bullet
from Scripts.environment import Environment, getBedrocks, getCoastColliderPoints, getCoastRects
from Scripts.collision import Collision
from Scripts.enemy import spawnEnemies, enemyAiUpdate


pygame.init()

# To create a window
screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
clock = pygame.time.Clock()

pygame.display.set_caption("Water Way Wars")

event = {}

txt = Text(screen, "Water Way Wars", (0, 0, 300, 100), 0, 100)
DescTxt = Text(screen, "Prevent the enemies for getting into our coast by shooting them. Move ahead and reach the there coast", (0, 0, 300, 100), 0, 30)
DescTxt2 = Text(screen, "Use wasd or arrows for control, space bar for trigger and +&- for zooming in and out", (0, 0, 300, 100), 1, 20)
wonTxt = Text(screen, "You Won !", (0, 0, 300, 100), 0, 100)
failedTxt = Text(screen, "Sorry, Your Failed !", (0, 0, 300, 100), 0, 100)
playTxt = Text(screen, "Press Enter to Play >>>", (0, 100, 300, 100), 1, 50)
fpsCounter = Text(screen, "fps: ", (0, 0, 300, 100), 1, 50)
debug = Text(screen, "fps: ", (0, 0, 300, 100), 1, 50)
playerSub = Submarine(screen, [-300, 0])
enemySet = []

worldCoord = [0, 0]
camMoveDelay = [100, 200]
scale = .3
popUp = True
won = False
failed = False

enemySet = spawnEnemies(screen, 10000, 100000, 0, 2000)


def Won():
    global won
    won = True

def Failed():
    global failed
    failed = True

def restart():
    global playerSub, enemySub, enemySet, scale
    playerSub = Submarine(screen, [-300, 0])
    enemySet = []
    scale = .3
    enemySet = spawnEnemies(screen, 10000, 100000, 0, 2000)


while True:
    event = eventLoop()

    dt = clock.tick()
    # print(mouse_buttons(), mouse_pos())
    scale += event['mouseY']*.001
    if event['minus']:
        scale -= .001 * dt
    if event['equal']:
        scale += .001 * dt
    scale = .05 if scale < .05 else scale
    scale = 2 if scale > 2 else scale

    screen.fill((255*.005, 255*.164, 255*.284))
    # screen.blit(pygame.transform.scale(bgImg, (bgImg.get_width()*2, bgImg.get_height()*2)), worldCoord)
    # screen.blit(bgImg, (round(worldCoord[0]), round(worldCoord[1])))
    Environment(screen, dt, worldCoord, scale, {
        'seaLevel': 0,
        'harbourPosX': -1000,
        'harbourLength': 2000,
        'harbourHeight': 50,
        'rocksPer1000px': 100,
        'minOceanDepth': 1500,
        'maxOceanDepth': 2000,
        'leftCoastPosX': -4000,
        'coastHeight': 100,
        'rightCoastPosX': 100000
    }, playerSub)

    txt.set_cent_pos(screen.get_width()//2, screen.get_height()//2)
    wonTxt.set_cent_pos(screen.get_width()//2, screen.get_height()//2)
    failedTxt.set_cent_pos(screen.get_width()//2, screen.get_height()//2)
    playTxt.set_cent_pos(screen.get_width()//2, screen.get_height()//2+100)
    DescTxt.set_cent_pos(screen.get_width()//2, screen.get_height()//2+50)
    DescTxt2.set_cent_pos(screen.get_width()//2, screen.get_height()//2-50)
    if popUp:
        txt.rend()
        playTxt.rend()
        DescTxt.rend()
        DescTxt2.rend()
    if won:
        wonTxt.rend()
        playTxt.rend()
    if failed:
        failedTxt.rend()
        playTxt.rend()
    if event['enter']:
        popUp = False
        failed = False
        won = False
        restart()
    fpsCounter.text = "fps: " + str(round(clock.get_fps())) + " dt: " + str(dt)
    fpsCounter.set_pos(40, 0)
    # fpsCounter.rend()
    # debug.text = "debug: " + str(playerSub.health)
    debug.text = "debug: " + str(round(playerSub.pos[0]))
    debug.set_pos(40, 70)
    # debug.rend()

    playerSub.update(event, worldCoord, dt, scale, 0)
    # Camera follower
    worldCoord[0] -= (playerSub.pos[0]+worldCoord[0])/camMoveDelay[0]*dt
    worldCoord[1] -= (playerSub.pos[1]+worldCoord[1])/camMoveDelay[1]*dt

    enemyAiUpdate(enemySet, playerSub, worldCoord, dt, scale)
    for i in enemySet:
        if i.health < 0:
            enemySet.remove(i)

    Collision(playerSub, enemySet, getBedrocks(), getCoastColliderPoints(), getCoastRects(), playerSub.bulletsSet, Won, Failed)
    # print([enemySub]+getBedrocks())

    pygame.display.update()
