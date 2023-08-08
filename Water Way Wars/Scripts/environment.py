import pygame
from Scripts.Objects import BedRock
import random
import math


depthMap = {}
coastClr = (.90*255, .73*255, .60*255)
leftCoastRect = None
rightCoastRect = None
leftCoastSlopPoints = None
rightCoastSlopPoints = None

def Environment(dis, dt, worldCoord, scale, parameters, player):
    global leftCoastRect, rightCoastRect, leftCoastSlopPoints, rightCoastSlopPoints
    # for i in range(5):
    #     for j in range(5):
    #         dis.blit(pygame.transform.scale(bgImg, (round(bgImg.get_width()*scale), round(bgImg.get_height()*scale))), (round((worldCoord[0] + i*bgImg.get_width())*scale) + dis.get_width()//2, round((worldCoord[1] + j*bgImg.get_height())*scale) + dis.get_height()//2))

    # Sky
    pygame.draw.rect(dis, (150, 180, 200), (0,
                                            0,
                                            dis.get_width(),
                                            dis.get_height()//2+round((parameters['seaLevel']+worldCoord[1])*scale)))
    # Harbour
    pygame.draw.rect(dis, (25, 30, 45), (dis.get_width()//2 + round((parameters['harbourPosX']-parameters['harbourLength']/2+worldCoord[0])*scale),
                                         dis.get_height()//2+round((worldCoord[1]-parameters['seaLevel']-parameters['harbourHeight'])*scale),
                                         round(parameters['harbourLength']*scale),
                                         dis.get_height()//2+round((parameters['seaLevel']-worldCoord[1]+parameters['harbourHeight'])*scale)))
    # Coast
    leftCoastRect = (
                dis.get_width()//2 + round((parameters['leftCoastPosX']+worldCoord[0]-10000)*scale),
                dis.get_height()//2 + round((parameters['seaLevel']-parameters['coastHeight']+worldCoord[1])*scale),
                round(10000*scale),
                dis.get_height() - dis.get_height()//2 - round((parameters['seaLevel']-parameters['coastHeight']+worldCoord[1])*scale)
                    )
    pygame.draw.rect(dis, coastClr, leftCoastRect)
    rightCoastRect = (
        dis.get_width()//2 + round((parameters['rightCoastPosX']+worldCoord[0])*scale),
        dis.get_height()//2 + round((parameters['seaLevel']+worldCoord[1])*scale),
        round(10000*scale),
        dis.get_height() - dis.get_height()//2 - round((parameters['seaLevel']+worldCoord[1])*scale)
                      )
    pygame.draw.rect(dis, coastClr, rightCoastRect)
    leftCoastSlopPoints = [
                        (dis.get_width()//2 + (parameters['leftCoastPosX']+worldCoord[0])*scale, dis.get_height()//2 + round((parameters['seaLevel']-parameters['coastHeight']+worldCoord[1])*scale)),
                        (dis.get_width()//2 + (parameters['leftCoastPosX']+worldCoord[0])*scale, dis.get_height()),
                        (dis.get_width()//2 + (parameters['leftCoastPosX']+worldCoord[0])*scale + 2*(dis.get_height() - dis.get_height()//2 - round((parameters['seaLevel']-parameters['coastHeight']+worldCoord[1])*scale)), dis.get_height())
                        ]
    pygame.draw.polygon(dis, coastClr, leftCoastSlopPoints)
    rightCoastSlopPoints = [
                        (dis.get_width()//2 + (parameters['rightCoastPosX']+worldCoord[0])*scale, dis.get_height()//2 + round((parameters['seaLevel']-parameters['coastHeight']+worldCoord[1])*scale)),
                        (dis.get_width()//2 + (parameters['rightCoastPosX']+worldCoord[0])*scale, dis.get_height()),
                        (dis.get_width()//2 + (parameters['rightCoastPosX']+worldCoord[0])*scale - 2*(dis.get_height() - dis.get_height()//2 - round((parameters['seaLevel']-parameters['coastHeight']+worldCoord[1])*scale)), dis.get_height())
                        ]
    pygame.draw.polygon(dis, coastClr, rightCoastSlopPoints)
    # Seabed
    for j in range(-round(dis.get_width()/1000/scale), round(dis.get_width()/1000/scale)+1):
        if player.pos[0]//1000+j in depthMap:
            for i in depthMap[player.pos[0] // 1000 + j]:
                i.update(worldCoord, scale, parameters['seaLevel'])
        else:
            depthMap[player.pos[0] // 1000 + j] = []
            r = random.randrange(5, 20)
            for i in range(parameters['rocksPer1000px']):
                depthMap[player.pos[0] // 1000 + j].append(BedRock(dis, [(player.pos[0]//1000+j)*1000 + 1000*i/parameters['rocksPer1000px'],
                                                                         dis.get_height()//2 + parameters['minOceanDepth'] + (parameters['maxOceanDepth']-parameters['minOceanDepth'])
                                                                         + (
                                                                         1/r*math.sin(12*math.pi*i/parameters['rocksPer1000px']) +
                                                                         2/r*math.sin(12/2*math.pi*i/parameters['rocksPer1000px']) +
                                                                         3/r*math.sin(12/6*math.pi*i/parameters['rocksPer1000px'])
                                                                            )*(parameters['maxOceanDepth']-parameters['minOceanDepth'])
                                                                         ],
                                                                   [random.randrange(10, 50), 50]))


def getBedrocks():
    d = []
    for i in depthMap.values():
        for j in i:
            d.append(j)
    return d


def lerp(a, b, t):
    return a+(b-a)*t


def getCoastColliderPoints():
    noOfPoints = 1000
    points1 = []
    points2 = []
    for i in range(noOfPoints):
        points1.append([
            lerp(leftCoastSlopPoints[0][0], leftCoastSlopPoints[2][0], i/(noOfPoints-1)),
            lerp(leftCoastSlopPoints[0][1], leftCoastSlopPoints[2][1], i/(noOfPoints-1))
        ])
    for i in range(noOfPoints):
        points2.append([
            lerp(rightCoastSlopPoints[0][0], rightCoastSlopPoints[2][0], i/(noOfPoints-1)),
            lerp(rightCoastSlopPoints[0][1], rightCoastSlopPoints[2][1], i/(noOfPoints-1))
        ])
    return [points1, points2]


def getCoastRects():
    return [leftCoastRect, rightCoastRect]
