from typing import get_type_hints
import numpy as np
import cvxpy as cp
import json

arr_pos = ['N', 'S', 'E', 'W', 'C']
arr_mat = [0, 1, 2]
arr_arrow = [0, 1, 2, 3]
arr_mm_state = ['R', 'D']
arr_health = [0, 25, 50, 75, 100]

INF = 100000000

# test_1 = 0
# test_2 = 0

state_num = []
states = []
len_states = 0
state_action_tuples = []

A = []
r = []
num_col = 0

policy = []

step_cost = -20

pos_actions = {'N': ("CRAFT", "DOWN", "STAY"), 'S': ("GATHER", "UP", "STAY"), \
'E': ("SHOOT", "HIT", "LEFT", "STAY"), 'W': ("SHOOT", "RIGHT", "STAY"), \
'C': ("SHOOT", "HIT", "UP", "DOWN", "LEFT", "RIGHT", "STAY")}


def initialize():
    global arr_arrow, arr_health, arr_mat, arr_mm_state, arr_pos
    global state_num
    global states, len_states
    states = []
    for pos in arr_pos:
        for mat in arr_mat:
            for arrow in arr_arrow:
                for state in arr_mm_state:
                    for health in arr_health:
                        states.append((pos, mat, arrow, state, health))
                        
    len_states = len(states)
    val_states = [i for i in range(0, len_states)]

    zip_iterator = zip(states, val_states)
    state_num = dict(zip_iterator)

def fill_north(state, action, col):
    global A
    global state_num

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    
    A[state_num[state]][col] = 1
    r[col] = step_cost
    # Craft
    if action == "CRAFT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('N', mat - 1, min(3, arrow + 1), 'D', health)]][col]  -= 0.50 * 0.8
            A[state_num[('N', mat - 1, min(3, arrow + 2), 'D', health)]][col]  -= 0.35 * 0.8
            A[state_num[('N', mat - 1, min(3, arrow + 3), 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('N', mat - 1, min(3, arrow + 1), 'R', health)]][col]  -= 0.50 * 0.2
            A[state_num[('N', mat - 1, min(3, arrow + 2), 'R', health)]][col]  -= 0.35 * 0.2
            A[state_num[('N', mat - 1, min(3, arrow + 3), 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('N', mat - 1, min(3, arrow + 1), 'D', health)]][col]  -= 0.50 * 0.50
            A[state_num[('N', mat - 1, min(3, arrow + 2), 'D', health)]][col]  -= 0.35 * 0.50
            A[state_num[('N', mat - 1, min(3, arrow + 3), 'D', health)]][col]  -= 0.15 * 0.50

            # Ready
            A[state_num[('N', mat - 1, min(3, arrow + 1), 'R', health)]][col]  -= 0.50 * 0.50
            A[state_num[('N', mat - 1, min(3, arrow + 2), 'R', health)]][col]  -= 0.35 * 0.50
            A[state_num[('N', mat - 1, min(3, arrow + 3), 'R', health)]][col]  -= 0.15 * 0.50

    # Move down
    if action == "DOWN":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.5
            
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5


    # Stay
    if action == "STAY":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('N', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8 ##
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('N', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('N', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.5
            
            #Ready
            A[state_num[('N', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5 ##
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5



def fill_south(state, action, col):
    global A
    global state_num

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    
    A[state_num[state]][col] = 1
    r[col] = step_cost
    # Craft
    if action == "GATHER":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('S', min(2, mat + 1), arrow, 'D', health)]][col]  -= 0.75 * 0.8 ##
            A[state_num[('S', mat, arrow, 'D', health)]][col]  -= 0.25 * 0.8 ##

            # Ready
            A[state_num[('S', min(2, mat + 1), arrow, 'R', health)]][col]  -= 0.75 * 0.2
            A[state_num[('S', mat, arrow, 'R', health)]][col]  -= 0.25 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('S', min(2, mat + 1), arrow, 'D', health)]][col]  -= 0.75 * 0.50
            A[state_num[('S', mat, arrow, 'D', health)]][col]  -= 0.25 * 0.50

            # Ready
            A[state_num[('S', min(2, mat + 1), arrow, 'R', health)]][col]  -= 0.75 * 0.50 ##
            A[state_num[('S', mat, arrow, 'R', health)]][col]  -= 0.25 * 0.50 ##

    # Move up
    if action == "UP":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.5
            
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5


    # Stay
    if action == "STAY":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('S', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8 ##
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('S', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('S', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.5
            
            #Ready
            A[state_num[('S', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5 ##
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5



def fill_east(state, action, col):
    global A
    global state_num

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]

    A[state_num[state]][col] = 1
    r[col] = step_cost
    # Shoot
    if action == "SHOOT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('E', mat, arrow-1, 'D', max(0, health-25))]][col]  -= 0.9 * 0.8
            A[state_num[('E', mat, arrow-1, 'D', health)]][col]  -= 0.1 * 0.8
            # Ready
            A[state_num[('E', mat, arrow-1, 'R', max(0, health-25))]][col]  -= 0.9 * 0.2
            A[state_num[('E', mat, arrow-1, 'R', health)]][col]  -= 0.1 * 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('E', mat, 0, 'D', min(100, health+25))]][col]  -= 1.0 * 0.5
            r[col] += (-40 * 0.5)
            # Be ready
            A[state_num[('E', mat, arrow-1, 'R', max(0, health-25))]][col]  -= 0.9 * 0.5
            A[state_num[('E', mat, arrow-1, 'R', health)]][col]  -= 0.1 * 0.5
    # Hit
    if action == "HIT":
        if mm_state == 'D':
            A[state_num[('E', mat, arrow, 'D', max(0, health-50))]][col]  -= 0.2 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.8 * 0.8 ##
            # Ready
            A[state_num[('E', mat, arrow, 'R', max(0, health-50))]][col]  -= 0.2 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.8 * 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('E', mat, 0, 'D', min(100, health+25))]][col]  -= 1.0 * 0.5
            r[col] += (-40 * 0.5)
            # Be ready
            A[state_num[('E', mat, arrow, 'R', max(0, health-50))]][col]  -= 0.2 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.8 * 0.5 ##
    # Left
    if action == "LEFT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 1.0 * 0.8
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 1.0 * 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('E', mat, 0, 'D', min(100, health+25))]][col]  -= 1.0 * 0.5
            r[col] += (-40 * 0.5)
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 1.0 * 0.5

    # Stay
    if action == "STAY":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 1.0 * 0.8 ##
            # Ready
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 1.0 * 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('E', mat, 0, 'D', min(100, health+25))]][col]  -= 1.0 * 0.5 ##
            r[col] += (-40 * 0.5)
            # Ready
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 1.0 * 0.5



def fill_west(state, action, col):
    global A
    global state_num

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]

    A[state_num[state]][col] = 1
    r[col] = step_cost

    # Shoot
    if action == "SHOOT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('W', mat, arrow-1, 'D', max(0, health-25))]][col]  -= 0.25 * 0.8
            A[state_num[('W', mat, arrow-1, 'D', health)]][col]  -= 0.75 * 0.8
            # Ready
            A[state_num[('W', mat, arrow-1, 'R', max(0, health-25))]][col]  -= 0.25 * 0.2
            A[state_num[('W', mat, arrow-1, 'R', health)]][col]  -= 0.75 * 0.2
        elif mm_state=='R':
            # Attack
            A[state_num[('W', mat, arrow-1, 'D', max(0, health-25))]][col]  -= 0.25 * 0.5
            A[state_num[('W', mat, arrow-1, 'D', health)]][col]  -= 0.75 * 0.5
            # Ready
            A[state_num[('W', mat, arrow-1, 'R', max(0, health-25))]][col]  -= 0.25 * 0.5
            A[state_num[('W', mat, arrow-1, 'R', health)]][col]  -= 0.75 * 0.5

    # Right
    if action == "RIGHT":   
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.8
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.5
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.5
    
    #Stay
    if action == "STAY":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('W', mat, arrow, 'D', health)]][col]  -= 0.8 ##
            # Ready
            A[state_num[('W', mat, arrow, 'R', health)]][col]  -= 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('W', mat, arrow, 'D', health)]][col]  -= 0.5 ##
            # Ready
            A[state_num[('W', mat, arrow, 'R', health)]][col]  -= 0.5

def fill_center(state, action, col):
    global A
    global state_num

    mat = state[1]
    arrow = state[2]
    mm_state = state[3]
    health = state[4]
    
    A[state_num[state]][col] = 1
    r[col] = step_cost

    # Shoot
    if action == "SHOOT":   
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow-1, 'D', max(0, health-25))]][col]  -= 0.5 * 0.8
            A[state_num[('C', mat, arrow-1, 'D', health)]][col]  -= 0.5 * 0.8
            # Ready
            A[state_num[('C', mat, arrow-1, 'R', max(0, health-25))]][col]  -= 0.5 * 0.2
            A[state_num[('C', mat, arrow-1, 'R', health)]][col]  -= 0.5 * 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(100, health+25))]][col]  -= 1.0 * 0.5
            r[col] += (-40 * 0.5)
            # Hit
            A[state_num[('C', mat, arrow-1, 'R', max(0, health-25))]][col]  -= 0.5 * 0.5
            A[state_num[('C', mat, arrow-1, 'R', health)]][col]  -= 0.5 * 0.5
    
    # Hit
    if action == "HIT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow, 'D', max(0, health-50))]][col]  -= 0.1 * 0.8
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.9 * 0.8
            # Ready
            A[state_num[('C', mat, arrow, 'R', max(0, health-50))]][col]  -= 0.1 * 0.2
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.9 * 0.2
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(100, health+25))]][col]  -= 1.0 * 0.5
            r[col] += (-40 * 0.5)
            # Hit
            A[state_num[('C', mat, arrow, 'R', max(0, health-50))]][col]  -= 0.1 * 0.5
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.9 * 0.5
    
    # Move up
    if action == "UP":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('N', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('N', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(health+25, 100))]][col]  -=  1.0 * 0.5
            r[col] += (-40 * 0.5)
            # Ready
            A[state_num[('N', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5

    # Down
    if action == "DOWN":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('S', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('S', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(health+25, 100))]][col]  -=  1.0 * 0.5
            r[col] += (-40 * 0.5)
            
            # Ready
            A[state_num[('S', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5
            

    # Stay
    if action == "STAY":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('C', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(health+25, 100))]][col]  -=  1.0 * 0.5
            r[col] += (-40 * 0.5)
            
            # Ready
            A[state_num[('C', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5


    # East
    if action == "RIGHT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(health+25, 100))]][col]  -=  1.0 * 0.5
            r[col] += (-40 * 0.5)
            
            # Ready
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5


    # West
    if action == "LEFT":
        if mm_state == 'D':
            # Be dormant
            A[state_num[('W', mat, arrow, 'D', health)]][col]  -= 0.85 * 0.8
            A[state_num[('E', mat, arrow, 'D', health)]][col]  -= 0.15 * 0.8

            # Ready
            A[state_num[('W', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.2
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.2
            
        elif mm_state == 'R':
            # Attack
            A[state_num[('C', mat, 0, 'D', min(health+25, 100))]][col]  -=  1.0 * 0.5
            r[col] += (-40 * 0.5)
            
            # Ready
            A[state_num[('W', mat, arrow, 'R', health)]][col]  -= 0.85 * 0.5
            A[state_num[('E', mat, arrow, 'R', health)]][col]  -= 0.15 * 0.5



def fill_col_A(state, action, col):
    p = state[0]
    if action == "NONE":
        A[state_num[state]][col] = 1.0
        return
    elif p == 'N':
        fill_north(state, action, col)
    elif p == 'S':
        fill_south(state, action, col)
    elif p == 'E':
        fill_east(state, action, col)
    elif p == 'W':
        fill_west(state, action, col)
    elif p == 'C':
        fill_center(state, action, col)

def get_st_act_vals():
    global states
    global state_action_tuples
    global pos_actions

    for state in states:
        mat = state[1]
        arrow = state[2]
        health = state[4]
        if health == 0:
            state_action_tuples.append((state, "NONE"))
            continue
        for action in pos_actions[state[0]]:
            if action == "SHOOT" and arrow <= 0:
                continue
            if action == "CRAFT" and mat <= 0:
                continue
            state_action_tuples.append((state, action))
    # print(len(state_action_tuples))         


def get_A_matrix():
    global states
    # global test_1, test_2
    col = 0
    for [state, action] in state_action_tuples:
        fill_col_A(state, action, col)
        col += 1
        # if [state, action] == [('C', 0, 1, 'R', 100), 'DOWN']:
        #     test_1 = col - 1
        # if [state, action] == [('C', 0, 1, 'R', 100), 'LEFT']:
        #     test_2 = col - 1



def get_alpha(start):
    ll = len(states)
    alpha = [0.0 for _ in range(0, ll)]
    alpha[state_num[start]] = 1.0
    return alpha


def initialise_LP():
    global states, state_action_tuples
    global A, r, num_col

    get_st_act_vals()

    len1 = len(state_action_tuples)
    len2 = len(states)

    A = [[0.0 for i in range(len1)] for j in range(len2)]
    A = np.array(A)
    r = [0.0 for i in range(len1)]
    get_A_matrix()
    num_col = len(state_action_tuples)

def run_LP(start_state):
    global len_states, num_col
    global A, r
    alpha = get_alpha(start_state)
    r = np.array(r)
    r = r.reshape((1, num_col))
    alpha = np.array(alpha)
    alpha = alpha.reshape((len_states, 1))
    
    x = cp.Variable(shape=(num_col, 1), name="x")

    print(A.shape)
    print(r.shape)
    print(x.shape)
    print(alpha.shape)

    constraints = [cp.matmul(A, x) == alpha, x>=0]
    objective = cp.Maximize(cp.sum(cp.matmul(r, x), axis=0))
    problem = cp.Problem(objective, constraints)

    solution = problem.solve()
    print("Solution: " + str(solution))

    print("X: "+ str(x.value))
    return x.value, solution

def print_policy(x):
    global state_action_tuples
    global policy
    # print(state_action_tuples)
    # print(x)
    zip_iterator = zip(state_action_tuples, x)
    zipped = dict(zip_iterator)
    for state in states:
        action = "NONE"
        st_act = -INF
        for (st, act) in state_action_tuples:
            if st == state:
                if st_act < zipped[(st, act)][0]:
                    st_act = zipped[(st, act)][0]
                    action = act
        policy.append([state, action])
    # print(policy)


if __name__ == "__main__":
    initialize()
    # start = ('W', 0, 0, 'D', 100)
    start = ('C', 2, 3, 'R', 100)
    initialise_LP()
    x, objective = run_LP(start)
    print_policy(x)

    # print(A.type())
    # print(r.type())
    # print(x.type())
    # print(policy.type())
    # print(objective.type())
    X = []
    for _ in x:
        X.append(round(_[0], 3))
    dictionary = {"a": A.tolist(), "r": r[0].tolist(), "alpha": get_alpha(start), "x": X, "policy": policy, "objective": objective}
    with open('outputs/part_3_output.json', 'w') as outfile:
        json.dump(dictionary, outfile)
    
    # print(x[state_num[('C', 0, 1, 'R', 100)]])
    # print(r)
    # print(x[test_1])
    # print(x[test_2])
    # run_LP(start)
    # print_policy()