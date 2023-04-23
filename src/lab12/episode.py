''' 
Lab 12: Beginnings of Reinforcement Learning
We will modularize the code in pygrame_combat.py from lab 11 together.

Then it's your turn!
Create a function called run_episode that takes in two players
and runs a single episode of combat between them. 
As per RL conventions, the function should return a list of tuples
of the form (observation/state, action, reward) for each turn in the episode.
Note that observation/state is a tuple of the form (player1_health, player2_health).
Action is simply the weapon selected by the player.
Reward is the reward for the player for that turn.
'''

import sys
from pathlib import Path

from lab11.pygame_combat import run_turn
from lab11.turn_combat import Combat

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

def run_episode(Player1, Player2):
    players = [Player1, Player2]
    currentGame = Combat()
    history = []
    while not currentGame.gameOver:
        observation = tuple(plyr.health for plyr in players)
        reward = run_turn(currentGame, Player1, Player2)
        #print("THIS IS RUN REWARD %d", reward)
        history.append((observation, Player1.weapon, reward))
    return history


    '''
    currentGame = Combat()

    output = []

    while not currentGame.gameOver:
        output.append((run_turn(currentGame, Player1, Player2)))
    
    return output
    '''
