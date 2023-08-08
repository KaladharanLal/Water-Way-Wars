import pygame


temp = [0, 0]


def Collision(player, movingObj, staticObj, staticPoints, staticRects, bullets, won, failed):
    for i in movingObj:
        if player.rect.colliderect(i.rect):
            temp[0] = i.velo[0]*i.mass
            temp[1] = i.velo[1]*i.mass
            i.velo[0] = player.velo[0]*player.mass/i.mass
            i.velo[1] = player.velo[1]*player.mass/i.mass
            player.velo[0] = temp[0]/player.mass
            player.velo[1] = temp[1]/player.mass
            player.health -= 1
            i.health -= 1
    for i in staticObj:
        if player.rect.colliderect(i.rect):
            player.velo[0] *= -1
            player.velo[1] *= -1
            player.health -= 1
        for j in movingObj:
            if j.rect.colliderect(i.rect):
                j.velo[0] *= -1
                j.velo[1] *= -1
                j.health -= 1
    for h in staticPoints:
        for i in h:
            if player.rect.collidepoint(i):
                player.velo[0] *= -1
                player.velo[1] *= -1
                player.health -= 1
                if staticPoints.index(h) == 1:
                    print("won")
                    won()
            for j in movingObj:
                if j.rect.collidepoint(i):
                    print("coll")
                    j.velo[0] *= -1
                    j.velo[1] *= -1
                    j.health -= 1
                    if staticPoints.index(h) == 0:
                        print("failed")
                        failed()
    for i in staticRects:
        if i:
            if player.rect.colliderect(pygame.Rect(i)):
                player.velo[0] *= -1
                player.velo[1] *= -1
                player.health -= 1
            for j in movingObj:
                if j.rect.colliderect(pygame.Rect(i)):
                    j.velo[0] *= -1
                    j.velo[1] *= -1
                    j.health -= 1
    for i in bullets:
        for j in movingObj:
            if j.rect.colliderect(i.rect):
                j.velo[0] *= -1
                j.velo[1] *= -1
                j.health -= 10

