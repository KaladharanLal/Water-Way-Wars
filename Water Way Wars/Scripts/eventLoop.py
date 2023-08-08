import pygame
import sys

left = False
right = False
up = False
down = False
space = False
mouseY = 0
minus = False
equal = False
enter = False


def eventLoop():
    global left, right, up, down, space, mouseY, minus, equal, enter
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                print("Left arrow is pressed")
                left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                print("Right arrow is pressed")
                right = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                print("Up arrow is pressed")
                up = True
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                print("Down arrow is pressed")
                down = True
            if event.key == pygame.K_SPACE:
                print("Space is pressed")
                space = True
            if event.key == pygame.K_MINUS:
                print("- is pressed")
                minus = True
            if event.key == pygame.K_EQUALS:
                print("+ is pressed")
                equal = True
            if event.key == pygame.K_RETURN:
                print("enter is pressed")
                enter = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                print("Left arrow is released")
                left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                print("Right arrow is released")
                right = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                print("Up arrow is released")
                up = False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                print("Down arrow is released")
                down = False
            if event.key == pygame.K_SPACE:
                print("Space is released")
                space = False
            if event.key == pygame.K_MINUS:
                print("- is released")
                minus = False
            if event.key == pygame.K_EQUALS:
                print("+ is released")
                equal = False
            if event.key == pygame.K_RETURN:
                print("enter is released")
                enter = False
        if event.type == pygame.MOUSEWHEEL:
            mouseY = event.y
        else:
            mouseY = 0
    return {'left': left, 'right': right, 'up': up, 'down': down, 'space': space, 'mouseY': mouseY, 'minus': minus, 'equal': equal, 'enter': enter}