#! /opt/homebrew/bin/python3.10

from math import sqrt
import random

# square info is stored in a tuple : (color, type/direction)
# colors are determined by letters

# directions for squares:
  #-1 : anchor      *
  # 0 : up/down     |
  # 1 : right/left  -
  # 2 : left/up     _|
  # 3 : right/up    |_
  # 4 : left/down   -|
  # 5 : right/down  |-

# determine if a state is solved and complete
def checker(state):
  visited = []
 
  # go through all the squares
  for i in range(len(state)):
    # if the square is an anchor and hasn't been visited, try to follow
    if state[i][1] == -1 and i not in visited:
      valid,path = follow_path(state,[], i)
      if not valid:
        return False
      # else, add the valid path to visited and continue
      visited += path

  # check that all squares have been visited
  if len(visited) == len(state):
    return True

# determines if anchor has a valid path and returns list of indices in the path
def follow_path(state, path, index):
  path_indices = path.copy()
  path_indices.append(index)

  # go through all the neighbors for the index
  for n in neighbors(state, index):
    # if the square isn't in the path and it is a valid move, try to follow it
    if n not in path_indices and validate_move(state, index, n):
      # if it is an anchor, then the path is complete, return valid and path
      if state[n][1] == -1:
        path_indices.append(n)
        return (True,path_indices)

      # otherwise, try to follow the path until it reaches an anchor
      v,p = follow_path(state, path_indices, n)
      if v:
        return (v,p)

  return(False,[])

# determines if a move is valid
def validate_move(state, index, neighbor):
  # check that the two squares are the same color
  if state[index][0] != state[neighbor][0]:
    return False
  
  i = state[index][1] 
  n = state[neighbor][1]

  # if neighbor is above the index
  if neighbor < index-1:
    if i in (-1,0,2,3) and n in (-1,0,4,5):
      return True

  # if neighbor is left of index
  if neighbor == index-1:
    if i in (-1,1,2,4) and n in (-1,1,3,5):
      return True

  # if neighbor is right of index
  if neighbor == index+1:
    if i in (-1,1,3,5) and n in (-1,1,2,4):
      return True

  # if neighbor is below index
  if neighbor > index+1:
    if i in (-1,0,4,5) and n in (-1,0,2,3):
      return True

  return False

# takes a state and index and returns all the valid neighbors for that index
#
# Didn't make any changes to neighbor_check, it is pretty ugly but works, so I'll make it nice later
def neighbors(state, index):
  length = len(state)
  size = int(sqrt(length))
  if index >= length:
    return None
  # if it is in the top row
  if index < size:
    # check if it is in left column
    if index % size == 0:
      return (index+1,index+size)
    # check if it is in the right column
    if (index+1) % size == 0:
      return (index-1,index+size)
    # if it isn't in a corner, return 3 neighbors
    return (index-1,index+1,index+size)


  # if it is in the bottom row
  if index >= length-size:
    # check if it is in left column
    if index % size == 0:
      return (index+1,index-size)
    # check if it is in the right column
    if (index+1) % size == 0:
      return (index-1,index-size)
    # if it isn't in a corner, return 3 neighbors
    return (index-1,index+1,index-size)

  # check if it is in the first column
  if index % size == 0:
    return (index-size, index+size, index+1)

  # check if it is in the last column
  if (index+1) % size == 0:
    return (index-size, index+size, index-1)

  # otherwise return all 4 neighbors

  return (index-size, index+size, index-1, index+1)

# open and read a puzzle file
def open_puzzle(filename):
  try:
    name = "./puzzles/l1/"+filename
    file = open(name, "r")
    f = file.read().splitlines()
    file.close()
    return f
  except IOError:
    print(filename + "does not exist in the puzzles folder")
    return
  
# given a puzzle.txt, return the state
def puzzle_to_state(filename):
  f = open_puzzle(filename)
  puzzle_size = len(f)
  
  tmp = ''
  for line in f:
    tmp += line
    
  final = []
  for char in tmp:
    if char != '.':
      final.append((char,-1))
    else:
      final.append((None,None))
  
  return final

# given a state, prints it in puzzle format
def print_puzz(state):
	side = int(len(state)**(1/2))

	for i in range(0, len(state), side):
			print(state[i:i+side])

def min_conflict_action_generator(i,state, colors):
  length = len(state)
  size = int(sqrt(length))

  if state[i][1] != -1:
    for c in colors:
      if i == 0:
        yield i,c,5
      elif i == size - 1:
        yield i,c,4
      elif i == length - size:
        yield i,c,3
      elif i == length -1:
        yield i,c,2
      # check columns
      elif i < size:
        yield i,c,1
        yield i,c,4
        yield i,c,5
      elif i > (length - size):
        yield i,c,1
        yield i,c,2
        yield i,c,3
      elif (i % size) == 0:
        yield i,c,0
        yield i,c,3
        yield i,c,5
      elif (i % size) == (size - 1):
        yield i,c,0
        yield i,c,2
        yield i,c,4
      else:
        for d in range(6):
          yield i,c,d

def action_generator(state, colors):
  length = len(state)
  size = int(sqrt(length))

  for i in range(len(state)):
    if state[i][1] != -1:
      for c in colors:
        if i == 0:
          yield i,c,5
        elif i == size - 1:
          yield i,c,4
        elif i == length - size:
          yield i,c,3
        elif i == length -1:
          yield i,c,2
        # check columns
        elif i < size:
          yield i,c,1
          yield i,c,4
          yield i,c,5
        elif i > (length - size):
          yield i,c,1
          yield i,c,2
          yield i,c,3
        elif (i % size) == 0:
          yield i,c,0
          yield i,c,3
          yield i,c,5
        elif (i % size) == (size - 1):
          yield i,c,0
          yield i,c,2
          yield i,c,4
        else:
          for d in range(6):
            yield i,c,d

def colors(state):
  colors = []
  for i in state:
    if i[1] == -1 and i[0] not in colors:
      colors.append(i[0])
  return colors 

# given an initial state, it returns a random state
def random_state(initial, colors):
  state = []
  length = len(initial)
  size = int(sqrt(length))
  
  for i in range(length):
    if initial[i][0] == None:
      # check corners
      if i == 0:
        state.append((random.choice(colors), 5))
      elif i == size - 1:
        state.append((random.choice(colors), 4))
      elif i == length - size:
        state.append((random.choice(colors), 3))
      elif i == length -1:
        state.append((random.choice(colors), 2))
      # check columns
      elif i < size:
        state.append((random.choice(colors), random.choice([1,4,5])))
      elif i > (length - size):
        state.append((random.choice(colors), random.choice([1,2,3])))
      elif (i % size) == 0:
        state.append((random.choice(colors), random.choice([0,3,5])))
      elif (i % size) == (size - 1):
        state.append((random.choice(colors), random.choice([0,2,4])))
      else:
        state.append((random.choice(colors), random.randint(0,5)))
    else:
      state.append((initial[i][0], -1))

  return state       
  

def do(state, action):
  i,c,d = action
  state[i] = (c,d)

def undo(state, action):
  i,c,d = action
  state[i] = (c,d)

# given an index, determine the neighbors that we want to check for valid color or direction
def interesting_neighbors(state,i,n):
  direction = state[i][1]
  if direction == -1:
    return True

  if direction == 0:
    if (n < i-1) or (n > i+1):
      return True

  if direction == 1:
    if (n == i-1) or (n == i+1):
      return True

  if direction == 2:
    if (n < i-1) or (n == i-1):
      return True

  if direction == 3:
    if (n < i-1) or (n == i+1):
      return True

  if direction == 4:
    if (n == i-1) or (n > i+1):
      return True

  if direction == 5:
    if (n == i+1) or (n > i+1):
      return True
  
def surrounded(state,i):
  surrounded = True
  for n in neighbors(state,i):
    if state[i][0] != state[n][0]:
      surrounded = False


def h(state):
  h = 0
  # count conflicts 0 for valid, -1 for invalid color, -1 for invalid pieces, -2 for both
  for i in range(len(state)):
    if state[i][1] != -1:
      # go through all the neighbors for the index
      for n in neighbors(state, i):
        if interesting_neighbors(state,i,n):
            if not validate_move(state,i,n):
              h+=1
    else:
      count = 0
      for n in neighbors(state, i):
        if validate_move(state,i,n):
          count += 1

      if count == 0:
        h+=1
      if count > 1:
        h+=count-1

  return h


# testing
state = [('r',-1),('g',5),('g',-1),('y',5),('y',-1),
         ('r',0),('g',0),('b',-1),('y',0),('o',-1),
         ('r',0),('g',0),('b',0),('y',0),('o',0),
         ('r',0),('g',-1),('b',0),('y',-1),('o',0),
         ('r',3),('r',-1),('b',-1),('o',-1),('o',2)]

bad_state = [('r',-1),('y',5),('g',-1),('y',5),('y',-1),
             ('g',3),('g',0),('g',-1),('r',0),('o',-1),
             ('b',0),('r',0),('b',0),('g',0),('r',0),
             ('0',0),('g',-1),('y',0),('y',-1),('b',0),
             ('r',3),('r',-1),('b',-1),('o',-1),('o',2)]
