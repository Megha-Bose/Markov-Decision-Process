from typing import get_type_hints
from numpy import Inf
import random
import sys


arr_pos = ['N', 'S', 'E', 'W', 'C']
arr_mat = [0, 1, 2]
arr_arrow = [0, 1, 2, 3]
arr_mm_state = ['R', 'D']
arr_health = [0, 25, 50, 75, 100]
utilities = None
prev_utilities = None

num_states = 0
states = None

visited = None
policy = []

step_cost = -20

discount = 0.25
delta = 0.001

INF = 100000000.0

def initialize():
    global arr_arrow, arr_health, arr_mat, arr_mm_state, arr_pos
    global utilities
    global prev_utilities
    global num_states
    global states
    global visited
    states = []
    for pos in arr_pos:
        for mat in arr_mat:
            for arrow in arr_arrow:
                for state in arr_mm_state:
                    for health in arr_health:
                        states.append((pos, mat, arrow, state, health))
                        
    num_states = len(states)
    # print(num_states)

    val_utilities = [(0, "NONE") for _ in range(0, num_states)]

    zip_iterator = zip(states, val_utilities)
    utilities = dict(zip_iterator)
    prev_utilities = utilities

    val_visited = [False for _ in range(0, num_states)]

    zip_iterator = zip(states, val_visited)
    visited = dict(zip_iterator)
    # print(utilities)
    # print(visited)


def find_south(state):
    global utilities
    global prev_utilities

    best = -INF
    val = 0
    best_move = "GATHER"

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    # Gather
    val = 0
    if mm_state == 'D':
        # Be dormant
        val += 0.75*0.8*prev_utilities[('S', min(2, mat + 1), arrow, 'D', health)][0]
        val += 0.25*0.8*prev_utilities[('S', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.75*0.2*prev_utilities[('S', min(2, mat + 1), arrow, 'R', health)][0]
        val += 0.25*0.2*prev_utilities[('S', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        #Attack
        val += 0.75*0.50*prev_utilities[('S', min(2, mat + 1), arrow, 'D', health)][0]
        val += 0.25*0.50*prev_utilities[('S', mat, arrow, 'D', health)][0]
        #Ready
        val += 0.75*0.50*prev_utilities[('S', min(2, mat + 1), arrow, 'R', health)][0]
        val += 0.25*0.50*prev_utilities[('S', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    best = max(best, val)

    # Move UP
    val = 0
    if mm_state == 'D':
        # Be dormant
        val += 0.85 * 0.8 * prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.2 * prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        # Attack
        val += 0.85 * 0.5 * prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.5 * prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    if val > best:
        best_move = "UP"
        best = val

    # Stay
    val = 0
    if mm_state == 'D':
        # Be dormant
        val += 0.85 * 0.8 * prev_utilities[('S', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.2 * prev_utilities[('S', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        # Attack
        val += 0.85 * 0.5 * prev_utilities[('S', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.5 * prev_utilities[('S', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    if val > best:
        best_move = "STAY"
        best = val
    return (best, best_move)


def find_north(state):
    global utilities
    global prev_utilities
    
    best = -INF
    val = 0
    best_move = "CRAFT"

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    # Craft
    val = 0
    if mat >= 1:
        if mm_state == 'D':
            # Be dormant
            val += 0.50 * 0.8 * prev_utilities[('N', mat - 1, min(3, arrow + 1), 'D', health)][0]
            val += 0.35 * 0.8 * prev_utilities[('N', mat - 1, min(3, arrow + 2), 'D', health)][0]
            val += 0.15 * 0.8 * prev_utilities[('N', mat - 1, min(3, arrow + 3), 'D', health)][0]
            # Ready
            val += 0.50 * 0.2 * prev_utilities[('N', mat - 1, min(3, arrow + 1), 'R', health)][0]
            val += 0.35 * 0.2 * prev_utilities[('N', mat - 1, min(3, arrow + 2), 'R', health)][0]
            val += 0.15 * 0.2 * prev_utilities[('N', mat - 1, min(3, arrow + 3), 'R', health)][0]
        elif mm_state == 'R':
            #Attack
            val += 0.50 * 0.50 * prev_utilities[('N', mat - 1, min(3, arrow + 1), 'D', health)][0]
            val += 0.35 * 0.50 * prev_utilities[('N', mat - 1, min(3, arrow + 2), 'D', health)][0]
            val += 0.15 * 0.50 * prev_utilities[('N', mat - 1, min(3, arrow + 3), 'D', health)][0]
            #Ready
            val += 0.50 * 0.50 * prev_utilities[('N', mat - 1, min(3, arrow + 1), 'R', health)][0]
            val += 0.35 * 0.50 * prev_utilities[('N', mat - 1, min(3, arrow + 2), 'R', health)][0]
            val += 0.15 * 0.50 * prev_utilities[('N', mat - 1, min(3, arrow + 3), 'R', health)][0]
        val = discount * val + step_cost
        best = max(best, val)

    # Move down
    val = 0
    if mm_state == 'D':
        # Be dormant
        val += 0.85 * 0.8 * prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.2 * prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        # Attack
        val += 0.85 * 0.5 * prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.5 * prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    if val > best:
        best_move = "DOWN"
        best = val

    # Stay
    val = 0
    if mm_state == 'D':
        # Be dormant
        val += 0.85 * 0.8 * prev_utilities[('N', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        # Ready
        val += 0.85 * 0.2 * prev_utilities[('N', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        # Attack
        val += 0.85 * 0.5 * prev_utilities[('N', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'D', health)][0]
        #Ready
        val += 0.85 * 0.5 * prev_utilities[('N', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    if val > best:
        best_move = "STAY"
        best = val
    return (best, best_move)
    

def find_east(state):
    global utilities
    global prev_utilities
    
    best = -INF
    val = 0
    best_move = "SHOOT"

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    # Shoot
    mm_shoot_dead = 0
    mm_hit_dead = 0

    if health - 25 <= 0:
        mm_shoot_dead = 50
    
    if health - 50 <= 0:
        mm_hit_dead = 50

    # Shoot
    if arrow >= 1:
        val = 0
        if mm_state == 'D':
            val += 0.9 * 0.8 * (discount * prev_utilities[('E', mat, arrow-1, 'D', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.1 * 0.8 * discount * prev_utilities[('E', mat, arrow-1, 'D', health)][0]
            val += 0.9 * 0.2 * (discount * prev_utilities[('E', mat, arrow-1, 'R', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.1 * 0.2 * discount * prev_utilities[('E', mat, arrow-1, 'R', health)][0]
        elif mm_state == 'R':
            val += 1.0 * 0.5 * (discount * prev_utilities[('E', mat, 0, 'D', min(100, health+25))][0] - 40)
            val += 0.9 * 0.5 * (discount * prev_utilities[('E', mat, arrow-1, 'R', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.1 * 0.5 * discount * prev_utilities[('E', mat, arrow-1, 'R', health)][0]
        val += step_cost
        best = max(best, val)

    # Hit
    val = 0
    if mm_state == 'D':
        val += 0.2 * 0.8 * (discount * prev_utilities[('E', mat, arrow, 'D', max(0, health-50))][0] + mm_hit_dead)
        val += 0.8 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.2 * 0.2 * (discount * prev_utilities[('E', mat, arrow, 'R', max(0, health-50))][0] + mm_hit_dead)
        val += 0.8 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        val += 1.0 * 0.5 * (discount * prev_utilities[('E', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.2 * 0.5 * (discount * prev_utilities[('E', mat, arrow, 'R', max(0, health-50))][0] + mm_hit_dead)
        val += 0.8 * 0.5 *  discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "HIT"
        best = val

    # Left
    val = 0
    if mm_state == 'D':
        val += 1.0 * 0.8 * discount *  prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 1.0 * 0.2 * discount *  prev_utilities[('C', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        val += 1.0 * 0.5 * (discount * prev_utilities[('E', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 1.0 * 0.5 * discount *  prev_utilities[('C', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "LEFT"
        best = val

    # Stay
    val = 0
    if mm_state == 'D':
        val += 1.0 * 0.8 * discount *  prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 1.0 * 0.2 * discount *  prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        val += 1.0 * 0.5 * (discount * prev_utilities[('E', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 1.0 * 0.5 * discount *  prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "STAY"
        best = val

    return (best, best_move)


def find_west(state):
    global utilities
    global prev_utilities
    
    best = -INF
    val = 0
    best_move = "SHOOT"

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    
    mm_shoot_dead = 0

    if health - 25 <= 0:
        mm_shoot_dead = 50

    # Shoot
    if arrow >= 1:
        val = 0
        if mm_state == 'D':
            val += 0.25*0.8 * (discount * prev_utilities[('W', mat, arrow-1, 'D', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.75*0.8 * discount * prev_utilities[('W', mat, arrow-1, 'D', health)][0]
            val += 0.25*0.2 * (discount * prev_utilities[('W', mat, arrow-1, 'R', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.75*0.2 * discount * prev_utilities[('W', mat, arrow-1, 'R', health)][0]
        elif mm_state=='R':
            val += 0.25*0.5 * (discount * prev_utilities[('W', mat, arrow-1, 'D', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.75*0.5 * discount * prev_utilities[('W', mat, arrow-1, 'D', health)][0]
            val += 0.25*0.5 * (discount * prev_utilities[('W', mat, arrow-1, 'R', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.75*0.5 * discount * prev_utilities[('W', mat, arrow-1, 'R', health)][0]
        val += step_cost
        best = max(best, val)

    # Right
    val = 0
    if mm_state == 'D':
        val = 0.2* prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.8*prev_utilities[('C', mat, arrow, 'D', health)][0]
    elif mm_state == 'R':
        val = 0.5* prev_utilities[ ('C', mat, arrow, 'D', health)][0]
        val += 0.5* prev_utilities[('C', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    if val > best:
        best_move = "RIGHT"
        best = val
    
    #Stay
    val = 0
    if state == 'D':
        val = 0.2*  prev_utilities[('W', mat, arrow, 'R', health)][0]
        val += 0.8* prev_utilities[('W', mat, arrow, 'D', health)][0]
    else:
        val = 0.5 * prev_utilities[('W', mat, arrow, 'D', health)][0]
        val += 0.5 *prev_utilities[('W', mat, arrow, 'R', health)][0]
    val = discount * val + step_cost
    if val > best:
        best_move = "STAY"
        best = val
    
    return (best, best_move)
    

def find_center(state):
    best = -INF
    val = 0
    best_move = "SHOOT"

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    
    mm_shoot_dead = 0
    mm_hit_dead = 0

    if health - 25 <= 0:
        mm_shoot_dead = 50
    
    if health - 50 <= 0:
        mm_hit_dead = 50

    # Shoot
    if arrow >= 1:
        val = 0
        if mm_state == 'D':
            val += 0.5 * 0.8 * (discount * prev_utilities[('C', mat, arrow-1, 'D', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.5 * 0.8 * discount * prev_utilities[('C', mat, arrow-1, 'D', health)][0]
            val += 0.5 * 0.2 * (discount * prev_utilities[('C', mat, arrow-1, 'R', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.5 * 0.2 * discount * prev_utilities[('C', mat, arrow-1, 'R', health)][0]
        elif mm_state == 'R':
            val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
            val += 0.5 * 0.5 * (discount * prev_utilities[('C', mat, arrow-1, 'R', max(0, health-25))][0] + mm_shoot_dead)
            val += 0.5 * 0.5 * discount * prev_utilities[('C', mat, arrow-1, 'R', health)][0]
        val += step_cost
        if val > best:
          best_move = "SHOOT"
          best = val

    # Hit
    val = 0
    if mm_state == 'D':
        val += 0.1 * 0.8 * (discount * prev_utilities[('C', mat, arrow, 'D', max(0, health-50))][0] + mm_hit_dead)
        val += 0.9 * 0.8 * discount * prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 0.1 * 0.2 * (discount * prev_utilities[('C', mat, arrow, 'R', max(0, health-50))][0] + mm_hit_dead)
        val += 0.9 * 0.2 * discount * prev_utilities[('C', mat, arrow, 'R', health)][0]
    elif mm_state == 'R':
        val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.1 * 0.5 * (discount * prev_utilities[('C', mat, arrow, 'R', max(0, health-50))][0] + mm_hit_dead)
        val += 0.9 * 0.5 * discount * prev_utilities[('C', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "HIT"
        best = val

    # Right
    val = 0
    if mm_state == 'D':
        val += 0.85 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.85 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R': 
        val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.85 * 0.5 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "RIGHT"
        best = val

    # Left
    val = 0
    if mm_state == 'D':
        val += 0.85 * 0.8 * discount * prev_utilities[('W', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.85 * 0.2 * discount * prev_utilities[('W', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R': 
        val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.85 * 0.5 * discount * prev_utilities[('W', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "LEFT"
        best = val
        
    # Up
    val = 0
    if mm_state == 'D':
        val += 0.85 * 0.8 * discount * prev_utilities[('N', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.85 * 0.2 * discount * prev_utilities[('N', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R': 
        val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.85 * 0.5 * discount * prev_utilities[('N', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "UP"
        best = val

    # Down
    val = 0
    if mm_state == 'D':
        val += 0.85 * 0.8 * discount * prev_utilities[('S', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.85 * 0.2 * discount * prev_utilities[('S', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R': 
        val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.85 * 0.5 * discount * prev_utilities[('S', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "DOWN"
        best = val

    # Stay
    val = 0
    if mm_state == 'D':
        val += 0.85 * 0.8 * discount * prev_utilities[('C', mat, arrow, 'D', health)][0]
        val += 0.15 * 0.8 * discount * prev_utilities[('E', mat, arrow, 'D', health)][0]
        val += 0.85 * 0.2 * discount * prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.2 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    elif mm_state == 'R': 
        val += 1.0 * 0.5 * (discount * prev_utilities[('C', mat, 0, 'D', min(100, health+25))][0] - 40)
        val += 0.85 * 0.5 * discount * prev_utilities[('C', mat, arrow, 'R', health)][0]
        val += 0.15 * 0.5 * discount * prev_utilities[('E', mat, arrow, 'R', health)][0]
    val += step_cost
    if val > best:
        best_move = "STAY"
        best = val

    return (best, best_move)
    
    
def get_max_utility(state):
    if (state[4]==0):
        return (0, "NONE")
    if state[0] == 'N':
        return find_north(state)
    elif state[0] == 'S':
        return find_south(state)
    elif state[0] == 'E':
        return find_east(state)
    elif state[0] == 'W':
        return find_west(state)
    elif state[0] == 'C':
        return find_center(state)


def get_max_diff():
    global states
    diff = 0.0
    for state in states:
        diff = max(diff, abs(utilities[state][0]-prev_utilities[state][0]))
        # print(utilities[state][0], " , ", prev_utilities[state][0])
    return diff

def find_next_north(state, action):
    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    pos_states = []
    if action == "CRAFT":
        pos_states.append(('N', mat-1, min(3, arrow+1), 'D', health))
        pos_states.append(('N', mat-1, min(3, arrow+1), 'R', health))
        pos_states.append(('N', mat-1, min(3, arrow+2), 'D', health))
        pos_states.append(('N', mat-1, min(3, arrow+2), 'R', health))
        pos_states.append(('N', mat-1, min(3, arrow+3), 'D', health))
        pos_states.append(('N', mat-1, min(3, arrow+3), 'R', health))
    elif action == "DOWN":
        pos_states.append(('C', mat, arrow, 'D', health))
        pos_states.append(('C', mat, arrow, 'R', health))
        pos_states.append(('E', mat, arrow, 'D', health))
        pos_states.append(('E', mat, arrow, 'R', health))
    elif action == "STAY":
        pos_states.append(('N', mat, arrow, 'D', health))
        pos_states.append(('N', mat, arrow, 'R', health))
        pos_states.append(('E', mat, arrow, 'D', health))
        pos_states.append(('E', mat, arrow, 'R', health))

    return pos_states

def find_next_south(state, action):
    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]

    pos_states = []
    
    if action == "GATHER":
        pos_states.append(('S', min(2, mat+1), arrow, 'D', health))
        pos_states.append(('S', min(2, mat+1), arrow, 'R', health))
        pos_states.append(('S', mat, arrow, 'D', health))
        pos_states.append(('S', mat, arrow, 'R', health))
    elif action == "UP":
        pos_states.append(('C', mat, arrow, 'D', health))
        pos_states.append(('C', mat, arrow, 'R', health))
        pos_states.append(('E', mat, arrow, 'D', health))
        pos_states.append(('E', mat, arrow, 'R', health))
    elif action == "STAY":
        pos_states.append(('S', mat, arrow, 'D', health))
        pos_states.append(('S', mat, arrow, 'R', health))
        pos_states.append(('E', mat, arrow, 'D', health))
        pos_states.append(('E', mat, arrow, 'R', health))
    return pos_states

def find_next_west(state, action):
    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    
    pos_states = []
    
    if action == "SHOOT":
        pos_states.append(('W', mat, arrow-1, 'R', health))
        pos_states.append(('W', mat, arrow-1, 'R', max(0, health-25)))
        pos_states.append(('W', mat, arrow-1, 'D', health))
        pos_states.append(('W', mat, arrow-1, 'D', max(0, health-25)))
    elif action == "RIGHT":
        pos_states.append(('C', mat, arrow, 'R', health))
        pos_states.append(('C', mat, arrow, 'D', health))
    elif action == "STAY":
        pos_states.append(('W', mat, arrow, 'R', health))
        pos_states.append(('W', mat, arrow, 'D', health))
    return pos_states

def find_next_east(state, action):
    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]

    pos_states = []

    if action == "SHOOT":
        if mm_state == 'D':
            pos_states.append(('E', mat, arrow-1, 'R', health))
            pos_states.append(('E', mat, arrow-1, 'R', max(0, health-25)))
            pos_states.append(('E', mat, arrow-1, 'D', health))
            pos_states.append(('E', mat, arrow-1, 'D', max(0, health-25)))
        elif mm_state == 'R':
            pos_states.append(('E', mat, arrow-1, 'R', health))
            pos_states.append(('E', mat, arrow-1, 'R', max(0, health-25)))
            pos_states.append(('E', mat, 0, 'D', health))
    elif action == "HIT":
        if mm_state == 'D':
            pos_states.append(('E', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', max(0, health-50)))
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'D', max(0, health-50)))
        elif mm_state == 'R':
            pos_states.append(('E', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', max(0, health-50)))
            pos_states.append(('E', mat, 0, 'D', health))
    elif action == "LEFT":
        if mm_state == 'D':
            pos_states.append(('C', mat, arrow, 'D', health))
            pos_states.append(('C', mat, arrow, 'R', health))
        elif mm_state == 'R':
            pos_states.append(('C', mat, arrow, 'R', health))
            pos_states.append(('E', mat, 0, 'D', health))
    elif action == "STAY":
        if mm_state == 'D':
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'R', health))
        elif mm_state == 'R':
            pos_states.append(('E', mat, arrow, 'R', health))
            pos_states.append(('E', mat, 0, 'D', health))
    return pos_states


def find_next_center(state, action):
    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]

    pos_states = []
    
    if action == "SHOOT":
        if mm_state == 'D':
            pos_states.append(('C', mat, arrow-1, 'D', max(0, health-25)))
            pos_states.append(('C', mat, arrow-1, 'D', health))
            pos_states.append(('C', mat, arrow-1, 'R', max(0, health-25)))
            pos_states.append(('C', mat, arrow-1, 'R', health))
        elif mm_state == 'R':
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('C', mat, arrow-1, 'R', max(0, health-25)))
            pos_states.append(('C', mat, arrow-1, 'R', health))
    
    elif action == "HIT":
        if mm_state == 'D':
            pos_states.append(('C', mat, arrow, 'D', max(0, health-50)))
            pos_states.append(('C', mat, arrow, 'D', health))
            pos_states.append(('C', mat, arrow, 'R', max(0, health-50)))
            pos_states.append(('C', mat, arrow, 'R', health))
        elif mm_state == 'R':
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('C', mat, arrow, 'R', max(0, health-50)))
            pos_states.append(('C', mat, arrow, 'R', health))
    
    elif action == "LEFT":
        if mm_state == 'D':
            pos_states.append(('W', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('W', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
        elif mm_state == 'R': 
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('W', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))

    elif action == "RIGHT":
        if mm_state == 'D':
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'R', health))
        elif mm_state == 'R': 
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('E', mat, arrow, 'R', health))

    elif action == "UP":
        if mm_state == 'D':
            pos_states.append(('N', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('N', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
        elif mm_state == 'R': 
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('N', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
    
    elif action == "DOWN":
        if mm_state == 'D':
            pos_states.append(('S', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('S', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
        elif mm_state == 'R': 
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('S', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
    
    elif action == "STAY":
        if mm_state == 'D':
            pos_states.append(('C', mat, arrow, 'D', health))
            pos_states.append(('E', mat, arrow, 'D', health))
            pos_states.append(('C', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
        elif mm_state == 'R': 
            pos_states.append(('C', mat, 0, 'D', min(100, health+25)))
            pos_states.append(('C', mat, arrow, 'R', health))
            pos_states.append(('E', mat, arrow, 'R', health))
    return pos_states

def get_next_states(state, action):
    pos_states = []
    if state[0] == 'N':
        pos_states = find_next_north(state, action)
    elif state[0] == 'S':
        pos_states = find_next_south(state, action)
    elif state[0] == 'E':
        pos_states = find_next_east(state, action)
    elif state[0] == 'W':
        pos_states = find_next_west(state, action)
    if state[0] == 'C':
        pos_states = find_next_center(state, action)
    return pos_states

def print_state_trace(state, value, action):
    pos =     state[0]
    mat =     state[1]
    arrow =   state[2]
    mm_state= state[3]
    health =  state[4]
    print("("+pos+","+str(mat)+","+str(arrow)+","+mm_state+","+str(health)+"):" + action + "=["+str(round(value, 3))+"]")



def get_policy(state):
    global visited
    global policy
    action = None
    if visited[state] == True:
        return
    visited[state] = True
    if state[4] == 0:
        policy.append((state, "FINISH"))
        return True
    action = get_max_utility(state)[1]

    next_states = get_next_states(state, action)
    random.shuffle(next_states)

    policy.append((state, action))

    reached = False
    for st in next_states:
        reached = get_policy(st)
        if reached:
            break
    if reached:
        return True
    visited[state] = False
    policy.pop()
    return False
    

def print_policy():
    global policy
    print("Printing policy")
    for i in range(len(policy)-1):
        pol = policy[i]
        state = pol[0]
        action = pol[1]
        print("From ", state, ", do action " + action + ".")

        pol = policy[i+1]
        state = pol[0]
        # action = pol[1]
        print("Reach state  ", state, ".")
        print()


def reset_visited():
    global policy, visited
    for k, v in visited.items():
        visited[k] = False
    policy.clear()

def run_iteration():
    global utilities    
    global prev_utilities
    global num_states
    global states
    not_converged = True
    num_iter = -1

    while not_converged:
        num_iter += 1
        prev_utilities = utilities.copy()
        print("iteration="+str(num_iter))
        for state in states:
            utilities[state] = get_max_utility(state)
            print_state_trace(state, utilities[state][0], utilities[state][1])

        max_diff = get_max_diff()
        # print("Max diff: ", max_diff)
        if max_diff < delta:
            not_converged = False
        # print("End of iteration " +str(num_iter)+ "\n")
    
    # print("\n\n\nPOLICY\n")
    # print("Policy for ('W', 0, 0, 'D', 100)\n")
    # reset_visited()
    # get_policy(('W', 0, 0, 'D', 100))
    # print_policy()
    # reset_visited()
    # print("Policy for ('C', 2, 0, 'R', 100)\n")
    # get_policy(('C', 2, 0, 'R', 100))
    # print_policy()



if __name__ == "__main__":
    initialize()
    sys.stdout = open('./outputs/part_2_task_2.3_trace.txt', 'w')
    run_iteration()
    sys.stdout.close()

