""" Create PyGameAIPlayer class here"""
import pygame
import random
from lab11.turn_combat import CombatPlayer


class PyGameAIPlayer:
    def __init__(self) -> None:
        pass

    #pick only possible routes that exist to traverse to
    def selectAction(self, state):
        possibleRoutes = [] 
        current = state.current_city
        for i in state.routes:
            if state.cities[current] == i[0]:
                for index, j in enumerate(state.cities):
                    if j == i[1]:
                        possibleRoutes.append(index)
            elif state.cities[current] == i[1]:
                for index, j in enumerate(state.cities):
                    if j == i[0]:
                        possibleRoutes.append(index)
            
       
        return ord(str(possibleRoutes[random.randint(0,len(possibleRoutes)-1)]))


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)

    def weapon_selecting_strategy(self):
            self.weapon = random.randint(0,2)
            return self.weapon
