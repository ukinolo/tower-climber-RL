from game import TowerClimberGame
import pygame
from typing import Any, SupportsFloat
import gymnasium as gym
from gymnasium import spaces
import numpy as np

class TowerClimberEnv(gym.Env):
    NUMBER_OF_IMPORTANT_FLOORS = 6

    def __init__(self, render_mode: str | None) -> None:
        super().__init__()
        metadata = {"render_modes": ["human", None]}
        self.game = TowerClimberGame(render_mode)


        # Actions:
        # 1: Jumping: Discrete(2) - NOOP[0], JUMP[1]
        # 2: Moving: Discrete(3) - NOOP[0], LEFT[1], RIGHT[2]
        self.action_space = spaces.MultiDiscrete(np.array([2, 3]), dtype=int)

        # self.observation_space = spaces.Dict({
        #     "agent": spaces.Box(np.array([0, -2000, 0]), np.array([self.game.WINDOW_WIDTH, self.game.WINDOW_HEIGHT, 1]), dtype=int),
        #     "important_floors_x": spaces.Box(np.full(shape=self.NUMBER_OF_IMPORTANT_FLOORS * 2, fill_value=0, dtype=int), np.full(shape=self.NUMBER_OF_IMPORTANT_FLOORS * 2, fill_value=self.game.WINDOW_WIDTH, dtype=int), dtype=int),
        #     "important_floors_y": spaces.Box(np.full(shape=self.NUMBER_OF_IMPORTANT_FLOORS * 2, fill_value=-9999, dtype=int), np.full(shape=self.NUMBER_OF_IMPORTANT_FLOORS * 2, fill_value=self.game.WINDOW_HEIGHT, dtype=int), dtype=int),
        # })

        self.observation_space = spaces.Dict({
            "agent": spaces.Box(low=0, high=1, shape=(3,), dtype=float),
            "important_floors_x": spaces.Box(low=0, high=1, shape=(self.NUMBER_OF_IMPORTANT_FLOORS * 2,), dtype=float),
            "important_floors_y": spaces.Box(low=0, high=1, shape=(self.NUMBER_OF_IMPORTANT_FLOORS * 2,), dtype=float),
        })

        self.score = 0.0
        self.previous_reward = 0.0
        self.reward = 0

    def _getState(self):
        agent_position = self.game.getPlayerPosition()
        agent_position[0] = agent_position[0]/self.game.WINDOW_WIDTH
        important_floors = self.game.getImportantFloors(self.NUMBER_OF_IMPORTANT_FLOORS)
        max_y = max(floor[1] for floor in important_floors)
        min_y = min(floor[1] for floor in important_floors)
        for floor in important_floors:
            floor[0] = floor[0]/self.game.WINDOW_WIDTH
            floor[1] = (floor[1]-min_y)/(max_y - min_y)
        agent_position[1] = max((agent_position[1]-min_y)/(max_y-min_y), 0)
        return {
            "agent": np.array(agent_position),
            "important_floors_x": np.array([floor[0] for floor in important_floors]),
            "important_floors_y": np.array([floor[1] for floor in important_floors]),
        }


    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        
        self.game.takeAction(action)

        #Update score
        self.score = self.game.getScore()
        self.reward = self.score - self.previous_reward
        self.previous_reward = self.score
        if(self.game.isEnd()):
            self.game.reset()

        return (self._getState(), self.reward, self.game.isEnd(), self.game.timePassed(), {})

    def reset(self, *, seed: int | None = None) -> tuple[Any, dict[str, Any]]:
        self.game.reset()
        self.score = 0.0
        self.previous_reward = 0.0
        self.reward = 0
        return (self._getState(), {})

    def render(self) -> None:
        self.game.drawOnScreen()
    
    def close(self) -> None:
        pygame.display.quit()
        pygame.quit()