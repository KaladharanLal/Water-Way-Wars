import random
from Scripts.Objects import Submarine


noOfEnemies = 10


def spawnEnemies(dis, startX, endX, high, low):
    global noOfEnemies
    enemySet = []
    for i in range(noOfEnemies):
        enemySet.append(Submarine(dis, [random.randrange(startX, endX), random.randrange(high, low)], (255, 0, 0)))
        enemySet[i].enemy = True
        enemySet[i].maxVelo = [random.randrange(3, 7)/10, .25]
    return enemySet

def enemyAiUpdate(enemySet, player, worldCoord, dt, scale):
    dir = [False, False, False, False] # left, up, right, down
    for i in enemySet:
        dir = [True, False, False, False]
        # if i.pos[0] > player.pos[0]:
        #     dir[0] = True
        # else:
        #     dir[2] = True
        # if i.pos[1] > player.pos[1]:
        #     dir[1] = True
        # else:
        #     dir[3] = True
        i.update({'up': dir[1], 'down': dir[3], 'left': dir[0], 'right': dir[2], 'space': False, }, worldCoord, dt, scale)
