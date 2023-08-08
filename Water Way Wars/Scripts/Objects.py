import pygame


class Submarine:
    def __init__(self, dis, pos, clr=(100, 200, 200)):
        self.dis = dis
        self.size = [200, 50]
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.rect.center = pos
        self.pos = pos
        self.velo = [0, 0]
        self.maxVelo = [2, .5]
        self.acc = [.001, .0008]
        self.drag = [.0005, .00035]
        self.breakForce = [.005, .007]
        self.clr = clr
        self.visible = True
        self.mass = 100
        self.bulletsSet = []
        self.shot = False
        self.enemy = False
        self.health = 100

    def update(self, event, worldCoord, dt, scale, seaLevel=0):
        if event["up"] and self.velo[1] > -self.maxVelo[1]:
            self.velo[1] -= self.acc[1]*dt
        if event["down"] and self.velo[1] < self.maxVelo[1]:
            self.velo[1] += self.acc[1]*dt
        if event["left"] and self.velo[0] > -self.maxVelo[0]:
            self.velo[0] -= self.acc[0]*dt
        if event["right"] and self.velo[0] < self.maxVelo[0]:
            self.velo[0] += self.acc[0]*dt
        if event["space"]:
            # self.velo[0] -= self.breakForce[0] * self.velo[0]/abs(self.velo[0]) if self.velo[0] != 0 else 0
            # self.velo[1] -= self.breakForce[1] * self.velo[1]/abs(self.velo[1]) if self.velo[1] != 0 else 0
            self.shot = True
        elif self.shot:
            self.bulletsSet.append(Bullet(self.dis, [self.pos[0], self.pos[1]]))
            self.bulletsSet[-1].enemyBullet = self.enemy
            self.shot = False
        self.pos[0] += self.velo[0]*dt
        self.pos[1] += self.velo[1]*dt
        self.velo[0] -= self.drag[0] * self.velo[0]/abs(self.velo[0]) * dt if self.velo[0] != 0 else 0
        self.velo[1] -= self.drag[1] * self.velo[1]/abs(self.velo[1]) * dt if self.velo[1] != 0 else 0
        self.rect.center = (round((self.pos[0]+worldCoord[0])*scale)+self.dis.get_width()//2, round((self.pos[1]+worldCoord[1])*scale)+self.dis.get_height()//2)
        self.rect.w = self.size[0]*scale
        self.rect.h = self.size[1]*scale
        if self.pos[1] < seaLevel:
            self.velo[1] += .00245 * dt

        # if self.pos[0] < -self.dis.get_width()//2:
        #     self.pos[0] += self.dis.get_width()
        # if self.pos[0] > self.dis.get_width()//2:
        #     self.pos[0] -= self.dis.get_width()
        # if self.pos[1] < -self.dis.get_height()//2:
        #     self.pos[1] += self.dis.get_height()
        # if self.pos[1] > self.dis.get_height()//2:
        #     self.pos[1] -= self.dis.get_height()

        for i in self.bulletsSet:
            if i.timer > 0:
                i.update(worldCoord, dt, scale)
            else:
                self.bulletsSet.remove(i)
        if self.visible:
            pygame.draw.rect(self.dis, self.clr, self.rect, 3)


class BedRock:
    def __init__(self, dis, pos, size=[100, 100], clr=(10, 20, 20)):
        self.dis = dis
        self.size = size
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.rect.center = pos
        self.pos = pos
        self.clr = clr
        self.visible = True

    def update(self, worldCoord, scale, seaLevel=0):
        if self.visible:
            pygame.draw.ellipse(self.dis, self.clr, self.rect)
            pygame.draw.rect(self.dis, self.clr, (self.rect.x, self.rect.y, self.rect.w, self.dis.get_height()-self.rect.y))
        self.rect.center = (self.dis.get_width()//2 + round((self.pos[0]+worldCoord[0]) * scale),
                            self.dis.get_height()//2 + round((self.pos[1]+worldCoord[1]) * scale))
        self.rect.w = self.size[0] * scale
        self.rect.h = self.size[1] * scale


class Bullet:
    def __init__(self, dis, pos, clr=(100, 100, 100)):
        self.dis = dis
        self.size = [50, 10]
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.rect.center = pos
        self.pos = pos
        self.velo = 1
        self.clr = clr
        self.visible = True
        self.mass = 1
        self.timer = 10000
        self.enemyBullet = False

    def update(self, worldCoord, dt, scale):
        self.pos[0] += self.velo*dt * (-1 if self.enemyBullet else 1)
        self.rect.center = (round((self.pos[0]+worldCoord[0])*scale)+self.dis.get_width()//2, round((self.pos[1]+worldCoord[1])*scale)+self.dis.get_height()//2)
        self.rect.w = self.size[0]*scale
        self.rect.h = self.size[1]*scale
        self.timer -= dt
        if self.visible:
            pygame.draw.rect(self.dis, self.clr, self.rect, 3)
