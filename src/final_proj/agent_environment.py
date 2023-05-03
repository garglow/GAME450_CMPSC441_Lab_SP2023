from collections import defaultdict
import sys
import numpy as np
import pygame
import random
from pathlib import Path
from transformers import pipeline
import random


sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))
from final_proj.pygame_combat import PyGamePolicyCombatPlayer, run_pygame_combat
from final_proj.pygame_ai_player import PyGameAICombatPlayer
from lab11.turn_combat import CombatPlayer
from lab13.rl_episodes import get_optimal_policy, run_episodes, test_policy
from final_proj.travel_cost import generate_terrain, get_route_cost
from lab11.landscape import get_elevation
from lab11.sprite import Sprite
from lab11.pygame_human_player import PyGameHumanPlayer
from lab11.landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


    
    
pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])


class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes


if __name__ == "__main__":
    budget = 1000
    size = width, height = 640, 480
    game_map = generate_terrain(size)
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_path = "assets/lego.png"
    sprite_speed = 1

    #initialize BERT unmasker, this is our pretrained Masked Language Model AI
    unmasker = pipeline("fill-mask", model="bert-base-uncased")
    result = "The current weather condition is [MASK]."
    sizeofmasks = len(unmasker(result))

    screen = setup_window(width, height, "Game World Gen Practice")

    #our relaistic cities are instantiated in our Genetic Algorithm AI and built here
    landscape_surface = get_landscape_surface(size)
    combat_surface = get_combat_surface(size)
    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    #elevation varibale added to get elevations for coordinates and pass thru
    #modified travel cost func
    elevation = []
    elevation = get_elevation(size)
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    player_sprite = Sprite(sprite_path, cities[start_city])

    

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    

    
    player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
    )

    #pretrain Legolas before he goes into battle, this is our Reinforcement Learning AI from lab13
    action_values = run_episodes(10000)
    optimal_policy = get_optimal_policy(action_values)
    

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:
            if int(chr(action)) != state.current_city and not state.travelling:
                start = cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = cities[state.destination_city]
                player_sprite.set_location(cities[state.current_city])
                state.travelling = True
                print(
                    "Travelling from", state.current_city, "to", state.destination_city
                )
                route_coordinate=(cities[state.current_city],cities[int(chr(action))])

                route_cost = get_route_cost(route_coordinate, game_map, elevation)

                #calculate budget
                print("Budget before arrival: $",budget)
                print("Route cost: $",route_cost)
                budget = round(budget-route_cost,2)
                print("Current budget: $",budget)

                #pick a randomly generated unmask from BERT
                random_number = random.randint(0, sizeofmasks-1)
                filled_result = unmasker(result)[random_number]['sequence']
                print(filled_result)

                if budget <= 0:
                    print("Legolas ran out of money! Game over.")
                    break

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)
        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        if not state.travelling:
            encounter_event = False
            state.current_city = state.destination_city

        if state.encounter_event:
            gameOver = run_pygame_combat(combat_surface, screen, player_sprite,optimal_policy)
            if gameOver == True:
                break
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()
        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
