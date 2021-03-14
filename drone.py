import pygame


class Drone:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.display_width = 780
        self.display_height = 780

    def drone_move(self, move_distace, choice):
        if choice == 0:  # left
            self.x -= move_distace
        if choice == 1:  # right
            self.x += move_distace
        if choice == 2:  # up
            self.y += move_distace
        if choice == 3:  # down
            self.y -= move_distace

        # if direction == pygame.K_LEFT:
        #     self.x -= move_distace
        # if direction == pygame.K_RIGHT:
        #     self.x += move_distace
        # if direction == pygame.K_DOWN:
        #     self.y += move_distace
        # if direction == pygame.K_UP:
        #     self.y -= move_distace
