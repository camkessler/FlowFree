#! /opt/homebrew/bin/python3.10
# Cam Kessler
from problem import *
from math import exp
from random import randint, random, choice

# Generates a random action.
def random_action(state,colors):
  actions = []
  for action in action_generator(state, colors):
    actions.append(action)
  return choice(actions)

# Considers a random change at each step.
# Accepts all positive changes and some negative changes.
# Stops after finding a goal state or reaching the minimum temperature.
# Returns the number of steps taken.
def simulated_annealing(state, colors, min_temp, cooling_rate):
    current_height = -h(state)
    temperature = 200.0
    steps = 0

    while temperature > min_temp and current_height < 0:
        action = random_action(state,colors)
        i = action[0]
        c,d = state[i][0], state[i][1]
        do(state, action)
        height = -h(state)

        temperature *= cooling_rate
        height_diff = height - current_height
        probability = exp(height_diff / temperature)

        if height > current_height or random() < probability:
            current_height = height
            steps += 1
        else:
            undo(state,(i,c,d))

    return steps,state

