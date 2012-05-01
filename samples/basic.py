import pygame

from beehive.core import Agent, SimpleVehicle
from beehive.geometry import Vector3
from beehive.steering import Seek, Flee

from honeycomb import Game
from honeycomb.controller import GameController
from honeycomb.event import Event
from honeycomb.model import GameModel
from honeycomb.view import GameView

SET_TARGET = 'set_target'
MODEL_UPDATE_START = 'model_update_start'
MODEL_UPDATE_COMPLETE = 'model_update_complete'


class DemoController(GameController):
    MOUSEBUTTONDOWN = {
        1: 'set_target',
        }

    def set_target(self, event):
        return Event(SET_TARGET, target=Vector3(*event.pos))


class DemoView(GameView):
    def __init__(self, manager):
        super(DemoView, self).__init__(manager, 640, 480)

    def on_model_update_complete(self, event):
        model = event.model
        x, y, _ = map(int, model.position)
        pygame.draw.circle(self.window, model.color, (x, y), model.radius)


class AgentModel(GameModel):
    def on_init(self, event):
        self.agent = Agent(body=SimpleVehicle())
        self.agent.learn(0.2, Seek)
        self.agent.learn(0.1, Flee)
        self.agent.target = self.agent.position
        self.agent.color = (255, 0, 0)
        self.agent.radius = 10

    def on_tick(self, event):
        self.dispatcher.dispatch(Event(MODEL_UPDATE_START))
        self.agent.update()
        self.dispatcher.dispatch(Event(MODEL_UPDATE_COMPLETE, model=self.agent))

    def on_set_target(self, event):
        target = event.target
        self.agent.target = target


def main():
    game = Game('Demo')
    game.add_controller(DemoController)
    game.add_view(DemoView)
    game.add_model(AgentModel)
    game.run()


if __name__ == '__main__':
    main()
