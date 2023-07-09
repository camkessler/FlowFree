#! /opt/homebrew/bin/python3.10
from problem import *
# Cam Kessler
# HW 2
#2/16/23

# makes the biggest improvement possible at each step.
# stops when no further improvements are possible
# returns the number of steps taken
def hill_climbing(state,colors):
  steps = 0
  while True:	
    best_height = -h(state)
    best_action = None

    for action in action_generator(state,colors):
      i = action[0]
      c,d = state[i][0], state[i][1]
      do(state, action)
      height = -h(state)

      if height > best_height:
        best_height = height
        best_action = action

      undo(state,(i,c,d))
     
    if best_action is not None:
      do(state, best_action)
      steps += 1
    else:
      return steps


state0 = puzzle_to_state("p1.txt")
cs = colors(state0)
done = False
count = 0
while not done:
  s = random_state(state0,cs)
  steps = hill_climbing(s,cs)
  done = checker(s)
  count += 1
print_puzz(s)
print(h(s))
print("count: ", count)
