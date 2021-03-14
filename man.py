import random


class Man:
    def __init__(self, size, color):
        self.size = size
        self.color = color

    def place_man(self, drone_x, drone_y, screen_width, screen_height):
        x = random.randint(0, (screen_width-self.size)//self.size)*self.size
        y = random.randint(0, (screen_height-self.size)//self.size)*self.size
        if x == drone_x and y == drone_y:
            self.place_man(self, drone_x, drone_y, screen_width, screen_height)
        return x, y

    def move_man(self, x, y, pixel_per_step, direction):
        if direction == 'left':
            x -= pixel_per_step
        if direction == 'right':
            x += pixel_per_step
        if direction == 'down':
            y += pixel_per_step
        if direction == 'up':
            y -= pixel_per_step

        return x, y
