import pygame
from drone import *
from man import *
import numpy as np
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time
pygame.init()

WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREY = (96, 96, 96)

BLOCK_SIZE = 20
BLOCK_VELOCITY = 20

screen_width = 200
screen_height = 200

MAN_FOUND_REWARD = 300
BOUNDARY_HIT_PENALTY = -200

NUM_EPISODE = 60000
SHOW_EVERY = 1000
epsilon = 0.9
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPS_DECAY = 0.9998

drone = Drone(20, screen_height - 40, BLOCK_SIZE, RED)
pygame_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Blocks')

#man = Drone(screen_width - 40, 20, BLOCK_SIZE, BLUE2)
man = Man(BLOCK_SIZE, BLUE1)
man_x, man_y = man.place_man(drone.x, drone.y, screen_width, screen_height)


# initialize q table
start_q_table = None  # can add a qtable file

if start_q_table is None:
    q_table = {}
    for x1 in range(0-20, screen_width+20 + 1, 20):
        for y1 in range(0-20, screen_height+20 + 1, 20):
            q_table[((x1, y1))] = [
                np.random.uniform(-5, 0) for i in range(4)]
else:
    with open(start_q_table, 'rb') as f:
        q_table = pickle.load(f)

print(f'{drone.x},{drone.y}')


def show_screen():

    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                drone.drone_move(BLOCK_VELOCITY, event.key)

                if(drone.x < 0 or drone.x >= screen_width or drone.y < 0 or drone.y >= screen_height):
                    print('out')

        pygame_display.fill(BLACK)

        pygame.draw.rect(pygame_display, drone.color, [
            drone.x, drone.y, drone.size, drone.size])
        pygame.draw.rect(pygame_display, man.color, [
            man_x, man_y, man.size, man.size])

        pygame.display.update()


def man_position(drone_x, drone_y, screen_width, screen_height):
    x = random.randint(0, (screen_width-man.size)//man.size)*man.size
    y = random.randint(0, (screen_height-man.size)//man.size)*man.size
    return x, y


episode_rewards = []
for episode in range(NUM_EPISODE):
    drone = Drone(20, screen_height - 40, BLOCK_SIZE, RED)
    #man = Man(BLOCK_SIZE, BLUE1)

    man_x, man_y = man_position(drone.x, drone.y, screen_width, screen_height)

    #print(drone.x, drone.y, screen_width, screen_height)
    # man_x = random.randint(0, (screen_width-man.size)//man.size)*man.size
    # man_y = random.randint(0, (screen_width-man.size)//man.size)*man.size

    if episode % SHOW_EVERY == 0:
        if episode == 0:
            continue
        else:
            print(f'Episode: {episode}, epsilon: {epsilon}')
            print(
                f'[{episode-SHOW_EVERY} episode to {episode} episode] mean is {np.mean(episode_rewards[-SHOW_EVERY:])}')
            print('')
            show = False

    else:
        show = False

    episode_reward = 0

    for i in range(200):
        obs = (drone.x, drone.y)
        if np.random.random() > epsilon:
            action = np.argmax(q_table[obs])
        else:
            action = np.random.randint(0, 4)

        drone.drone_move(BLOCK_SIZE, action)
        time.sleep(0.000)  # add delay here to see drone move
        #print(drone.x, drone.y, action, episode_reward)
        pygame_display.fill(BLACK)
        pygame.draw.rect(pygame_display, man.color, [
            man_x, man_y, man.size, man.size])
        pygame.draw.rect(pygame_display, drone.color, [
            drone.x, drone.y, drone.size, drone.size])

        pygame.display.update()

        if drone.x == man_x and drone.y == man_y:
            reward = MAN_FOUND_REWARD

        elif(drone.x < 0 or drone.x >= screen_width or drone.y < 0 or drone.y >= screen_height):
            reward = BOUNDARY_HIT_PENALTY
            # print('::::::OUT:::::')
        else:
            reward = -1

        new_obs = (drone.x, drone.y)
        max_future_q = np.max(q_table[new_obs])  # max Q value for this new obs
        current_q = q_table[obs][action]  # current Q for our chosen action

        if reward == MAN_FOUND_REWARD:
            new_q = MAN_FOUND_REWARD

        elif reward == BOUNDARY_HIT_PENALTY:
            new_q = BOUNDARY_HIT_PENALTY

        else:
            new_q = (1 - LEARNING_RATE) * current_q + \
                LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        q_table[obs][action] = new_q

        if show:
            show_screen()  # todo

        episode_reward += reward
        if reward == MAN_FOUND_REWARD or reward == BOUNDARY_HIT_PENALTY:
            break

    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(q_table, f)

moving_avg = np.convolve(episode_rewards, np.ones(
    (SHOW_EVERY,))/SHOW_EVERY, mode='valid')
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f'reward {SHOW_EVERY} moving avg')
plt.xlabel('episode number')
plt.savefig('graph.png')
plt.show()
