import random

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

from beehive.core import Agent, Shape, World
from beehive.geometry import Vector2
from beehive.steering import Seek


class PyGameWorld(World):
    def __init__(self, screen):
        self.screen = screen
        self.agents = {}

    def add(self, agent, shape=None):
        # initialize at random position
        w, h = self.size
        x, y = random.random() * w, random.random() * h
        agent.position = Vector2(x, y)

        # add agent-shape mapping
        self.agents[agent] = shape

    def update(self):
        for agent, shape in self.agents.items():
            # update agent position
            agent.update()

            # wrap around
            w, h = self.size
            x, y = agent.position
            agent.position = Vector2(x % w, y % h)

            # draw
            shape.draw(self.screen, agent.position)

    @property
    def size(self):
        w, h = self.screen.get_size()
        return Vector2(w, h)


class PyGameCircle(Shape):
    def __init__(self, color=None):
        if color is None:
            color = (255, 255, 255)
        self.color = color

    def draw(self, screen, position):
        # get screen coordinates
        position = map(int, position)
        pygame.draw.circle(screen, self.color, position, 10)


def main_pygame():
    # initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Demo')

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))

    # game objects
    clock = pygame.time.Clock()
    world = PyGameWorld(screen)
    shape = PyGameCircle(color=(255, 0, 0))
    agent = Agent()
    agent.learn(1.0, Seek)
    world.add(agent, shape)

    # main loop
    while True:
        clock.tick(60)

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                agent.target = Vector2(*event.pos)

        # prepare display
        screen.blit(background, (0, 0))
        # update world
        world.update()
        # refresh display
        pygame.display.flip()


if __name__ == '__main__':
    main_pygame()
