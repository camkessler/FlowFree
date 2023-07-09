#! /opt/homebrew/bin/python3.10
# Cam Kessler
from problem import *
from min_conflicts import *
import time
from annealing import *

state0 = puzzle_to_state("p3.txt")
cs = colors(state0)

mc_total_time = 0.00
mc_heur = 0
mc_solved = 0

sa_total_time = 0.00
sa_heur = 0
sa_solved = 0
for i in range(10):
  s = random_state(state0,cs)
  mc_state = s.copy()
  mc_t1 = time.perf_counter()
  puzz = min_conflicts(mc_state, cs, 40000, .02)
  mc_t2 = time.perf_counter()
  mc_total_time += (mc_t2-mc_t1)
  h1 = h(puzz)
  mc_heur += (h1)
  if h1 == 0:
    mc_solved += 1

  sa_state = s.copy()
  sa_t1 = time.perf_counter()
  step,state = simulated_annealing(sa_state,cs, 0.01, 0.999)
  sa_t2 = time.perf_counter()
  sa_total_time += (sa_t2-sa_t1)
  h2 = h(state)
  sa_heur += (h2)
  if h2 == 0:
    sa_solved += 1



print("MinConflicts------------\n","avg time: ", mc_total_time/10, "avg score: ", mc_heur/10, "solved: ", mc_solved)
print("SimAnnealing------------\n","avg time: ", sa_total_time/10, "avg score: ", sa_heur/10, "solved: ", sa_solved)
