#! /opt/homebrew/bin/python3.10
# Cam Kessler
from problem import *
from min_conflicts import *
import time

state0 = puzzle_to_state("p2.txt")
cs = colors(state0)

total_time = 0.00
heur = 0
solved = 0
for i in range(10):
  s = random_state(state0,cs)
  t1 = time.perf_counter()
  puzz = min_conflicts(s, cs, 40000, .02)
  t2 = time.perf_counter()
  total_time += (t2-t1)
  h1 = h(puzz)
  heur += (h1)
  if h1 == 0:
    solved += 1

print("avg time: ", total_time/10, "avg score: ", heur/10, "solved: ", solved)
