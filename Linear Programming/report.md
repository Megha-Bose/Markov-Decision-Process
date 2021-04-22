# Linear Programming

In the given problem, every state has 5 different values which are stored in tuples. The tuple is of the form < position, material, arrow, state, mm_health > which represents each state.

## LP formulation
We formulate the given problem as a Linear Program:
'state_action_tuples' contains each pair of states and the valid actions from those states. We make it using get_st_act_vals() function. 'pos_actions' is dictionary containing potential possible actions for each position value.

```
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

```

For each state-action pair (s, a), the reward vector r is the value of expected reward on taking the action a from state s.

The matrix A has dimension of number of states X length of state_action_tuples.

Vector alpha of size equal to number of states contains the initial probabilities of being in each state.
In our case, we will be dealing with definite start states and hence the value in alpha corresponding to the given start state will be 1.0 while others will be 0.0.

The problem is formulated as follows:

**maximise rx given Ax = alpha, x >= 0**

Here, each values in x corresponds to the expected number of times action a is taken in state s for state-action pair (s, a).


This problem can be related to the max flow problem. Here we are trying to maximise the reward while satisfying the flow constraint in flow = out flow.
A way of writing our LP problem is as follows:
For state j,

out flow = in flow

expected number of times action a is taken in state j summed over all possible actions - initial probability of being in state j 
= expected number of times state j is reached from state i using action a summed over all possible i, a pair

=> expected number of times action a is taken in state j summed over all possible actions - expected number of times state j is reached from state i using action a summed over all possible i, a pair 
= initial probability of being in state j 

=> sum_a (x_ja) - sum_i(sum_a(x_ia * p_i,a,j)) = alpha_j

After refactoring the above equation, we get

sum_i(sum_a(delta_ij - p_i,a,j) * x_ia) = alpha_j
(delta being Kronecker delta)
which is equivalent to the Ax = alpha constraint


## Procedure of making A matrix.

For each state action pair, (s, a),
1. The value in A corresponding to s is initialised as 1.0
2. We find the probability p of going to next state s' and the corresponding value in matrix A becomes -p
3. If p is the probability of ending up in the same state s, i.e., s = s', the corresponding value in matrix A becomes 1-p
4. We get A matrix using the get_A_matrix() function that fills each column corresponsing to a state-action pair using fill_col_A(state, action, col) function.

  ```
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
  
  def get_A_matrix():
      global states
      global test_1, test_2
      col = 0
      for [state, action] in state_action_tuples:
          fill_col_A(state, action, col)
          col += 1
  ```
  
  5. The functions fill_north(), fill_south(), fill_east(), fill_west() and fill_center() are chosen based on IJ's position to update the values of the columns of A matrix with values as described in points 1, 2 and 3.

## Procedure of finding the policy and analyze the results.

After calculating the value of x that gives the optimal value of rx, for each state, we select the action a out of possible (s, a) pairs that gives the highest x value. Higher x value means that the expected number of times the action is chosen is higher and hence we calculate the policy that selects the most probable action from each state in the print_policy(x) function.

```
def print_policy(x):
    global state_action_tuples
    global policy
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
    print(policy)
```

We store the policy in the output file, ./outputs/part_3_output_json, generated on executing part_3.py.

At first we thought that since this part has no positive reward for killing the monster, staying in the west could be a favourable policy. But, staying in the west will still incur the step cost each time. 

When we looked at the policy generated we saw that IJ tries to enter the east position in order to maximise the chances of killing the monster. The trend of aiming to kill the monster continued as that would end the game and subsequently avoid incurring further step costs or losses.


## Possiility of finding multiple policies

- Multiple policies can exist since for a particular state, there may be more than one possible actions with same x value.
- Instead of updating the best action if the current value is strictly greater than the best x value till now, we can make the inequality >=. This will select the last best action encountered instead of the first best action.
- We can also see that the order of actions considered while selecting the best policy affects the policy chosen if mutiple possible actions have same x value for the same state.

### Associated changes ( in terms of how they affect the A matrix, R vector, alpha vector etc.)

- If different policies are generated by changing the order of actions considered, it will shuffle the columns of matrix A.
- Similarly it will just shuffle values in reward vector r.
- We are keeping the order of states intact, so alpha won't be affected in this case.
- Different policies won't affect the final reward we get as the maximum value of rx doen't depend on the order of actions taken or whether strict inequality is used or not for selecting the best action for a state in the policy.

