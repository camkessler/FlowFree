#! /opt/homebrew/bin/python3.10
# Cam Kessler
from problem import *
from annealing import *


"""

puzzles = ["p1.txt","p2.txt"]
avg_steps = []
for p in puzzles:
  state = puzzle_to_state(p)
  print_puzz(state)
  cs = colors(state)
  steps = 0
  solved = 0
  for i in range(20):
    s = random_state(state, cs)
    step,state = simulated_annealing(s, cs, 0.01, 0.999)
    done = checker(s)
    steps += step
    solved += 1
  avg_steps.append(steps/20,solved)
    


"""
state0 = puzzle_to_state("p2.txt")
cs = colors(state0)
avg_count = 0
avg_steps = 0
for i in range(20):
  done = False
  steps = 0
  count = 0
  while not done:
    s = random_state(state0,cs)
    step,state = simulated_annealing(s,cs, 0.01, 0.999)
    done = checker(s)
    count += 1
    steps += step
  avg_count += count
  avg_steps += (steps/count)
print("count: ", avg_count)
print("steps: ", avg_steps/avg_count)
