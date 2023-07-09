#! /opt/homebrew/bin/python3.10
from problem import *
from random import random, choice

# Generates a random action.
def random_action(state,colors):
  actions = []
  for action in action_generator(state, colors):
    actions.append(action)
  return choice(actions)

def random_conflict(state):
  conflicting_indices = []
  for i in range(len(state)):
    if state[i][1] != -1:
      # go through all the neighbors for the index
      for n in neighbors(state, i):
        if interesting_neighbors(state,i,n):
            if not validate_move(state,i,n):
              if n not in conflicting_indices:
                if state[n][1] != -1:
                  conflicting_indices.append(n)
                conflicting_indices.append(i)
    else:
      seen = False
      count = 0
      for n in neighbors(state, i):
        if validate_move(state,i,n):
          if seen:
            if n not in conflicting_indices:
              if state[n][1] != -1:
                conflicting_indices.append(n)
          seen = True
          count += 1

      if count == 0:
        for n in neighbors(state, i):
          if n not in conflicting_indices:
            if state[n][1] != -1:
              conflicting_indices.append(n)

  return choice(conflicting_indices)

def minimize_conflicts(conflict, original_state, colors):
  state = original_state.copy()
  best_h = h(state)
  best_action = None
  
  for action in min_conflict_action_generator(conflict, state, colors):
    do(state, action)
   
    height = h(state)
    if height < best_h:
      best_h = height
      best_action = action

  return best_action

def min_conflicts(state, colors, max_steps, probability):
  for i in range(max_steps):
    if h(state) == 0:
      return state

    conflict = random_conflict(state)
    action = minimize_conflicts(conflict, state, colors) 
    if action != None:
      do(state, action)

    # added a little place for the algorithm to escape local minima
    if random() < probability:
      action = random_action(state,colors)
      do(state,action)
   
  return state
