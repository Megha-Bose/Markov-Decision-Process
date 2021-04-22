# Part 1 - Value Iteration

## Task 1

### Choice of actions for the states

We choose the action for a state which gives the highest utility for a particular state in a particular iteration. The utilities are calculated using Bellman update equation.

One significant observation we can make is that arrows have a higher probability of hitting the monster. The probability of an arrow hitting a monster is 0.25, 0.5, and 0.8 from West, Center, and East respectively. The damage an arrow can make is 0.25. But an important thing to note here is that getting attacked by a monster will result in a loss of all arrows IJ have at any moment. So in order to get arrows, he would have to go to North and CRAFT them, if he has material. Otherwise, he would have to go to South to GATHER material.

But IJ has one more form of attack, it's using a blade. His blade is never lost. Even though the probability of hitting by blade is low, it causes a damage of 50, double of that of an arrow. One more thing to note is that the probability of hitting Monster with blade from East is 0.2, which is twice the probability of hitting from Center.

So we can see a common pattern from states that if it doesn't have any arrows at the moment, it tries to move to the East in order to HIT with the blade.

We can notice this in multiple parts of the trace output. Let's see some examples.

`(C, 0, 3, D, 25):RIGHT=[-20.917]`

`(C, 0, 3, D, 50):RIGHT=[-93.731]`

`(C, 0, 3, D, 75):RIGHT=[-187.033]`

`(C, 0, 3, D, 100):RIGHT=[-309.047]`

`(S, 0, 3, R, 25):STAY=[-92.686]`

`(S, 0, 3, R, 50):STAY=[-178.382]`

`(S, 0, 3, R, 75):STAY=[-267.644]`

`(S, 0, 3, R, 100):STAY=[-373.079]`

`(W, 0, 2, D, 25):RIGHT=[-73.558]`

`(W, 0, 2, D, 50):RIGHT=[-168.469]`

`(W, 0, 2, D, 75):RIGHT=[-304.553]`

`(W, 0, 2, D, 100):RIGHT=[-358.437]`

If the monster was ready in the 4 states above, IJ would have tried to SHOOT or STAY and it will wait for the monster to become Dormant. 

`(N, 0, 2, D, 25):DOWN=[-65.791]`

`(N, 0, 2, D, 50):DOWN=[-159.591]`

`(N, 0, 2, D, 75):DOWN=[-297.632]`

`(N, 0, 2, D, 100):DOWN=[-352.602]`

The examples above shows the state when the Monster is dormant. This is because when the monster is ready, IJ tends to avoid immediate danger if possible. If avoiding it totally is not possible, IJ tends to find ways to easily reach East using teleportation. This will be clear with the examples that follow.


One other pattern is that, from the North and South, IJ tends to move to East. Let's see with examples:

`(N, 2, 3, R, 25):STAY=[-92.611]`

`(N, 2, 3, R, 50):STAY=[-177.43]`

`(N, 2, 3, R, 75):STAY=[-267.644]`

`(N, 2, 3, R, 100):STAY=[-373.079]`

Here, IJ is choosing `STAY` because going to down is may become destructive because Monster is ready. So ideally, he should `STAY` until Monster becomes Dormant. But if just staying on North was the aim, IJ should've selected `CRAFT`. Because, crafting will ensure that he will stay in North. Here, IJ is choosing `STAY` because he wants to reach East without going to Center. This can be seen clearly from the following example from trace.

`(C, 2, 3, D, 25):RIGHT=[-20.917]`

`(C, 2, 3, D, 50):RIGHT=[-93.731]`

`(C, 2, 3, D, 75):RIGHT=[-187.033]`

`(C, 2, 3, D, 100):RIGHT=[-309.047]`

Here, even after having arrows, it's trying to reach East. There are two reasons for this:

1. East gives the highest probability (0.9) for the arrows to hit.

2. Even if arrows are lost because of Monster's attack, East gives the highest probability (0.2) for IJ to kill the Monster using blade. We have already observed previously that going to East to attack with the blade is mostly the best option when we don't have arrows.



### Actions from North

1. If the number of arrows and materials we have is zero, going to the east and killing the monster is a better strategy than trying to gather materials, create arrows, and try to damage the monster with it.
2. If the number of arrows is greater than or equal to 1, IJ tries to stay in the north when the monster is in ready state but when the monster is dormant, IJ tries to move down.
3. WHen IJ has no arrows but has non zero number of materials, he tries to craft arrows.
4. When IJ has non zero number of 


### Method we used to find policy
We have a `state-utility` map. After convergence, we find the best action we can choose. This action can give us different possible next states. We first shuffle these and then try to recursively get a policy that reaches an end state using depth first search. 

### Policies for given start states

#### 1. (W, 0, 0, D, 100)

From  ('W', 0, 0, 'D', 100) , do action RIGHT.
Reach state   ('C', 0, 0, 'R', 100)

From  ('C', 0, 0, 'R', 100) , do action RIGHT.
Reach state   ('C', 0, 0, 'D', 100)

From  ('C', 0, 0, 'D', 100) , do action RIGHT.
Reach state   ('E', 0, 0, 'D', 100)

From  ('E', 0, 0, 'D', 100) , do action HIT.
Reach state   ('E', 0, 0, 'R', 50)

From  ('E', 0, 0, 'R', 50) , do action HIT.
Reach state   ('E', 0, 0, 'R', 0)

This is one of the best policies we have where IJ travels to the East square from West and HITS monster with blade. IJ is travelling to the East so that he has a higher probability to damage the monster with a blade in East. Probablility of hitting with a blade from East is 0.2 while that from Center is 0.1. So the chance of hitting monster from East is twice than that from Center. This is the reason for why IJ is travelling to the East.

One other thing to note here is that initially, IJ have no arrows with him. Even if he had, the maximum number of arrows he could have is 3 which can inflict a damage of 75. After that IJ will have to go to South to gather Material and then go to North to CRAFT an arrow in order to attack IJ. So even if IJ had 3 arrows in the beginning, trying to kill Monster using arrows will require more number of steps. That is the reason why IJ is moving to the East to kill Monster.


#### 2. (C, 2, 0, R, 100)

From  ('C', 2, 0, 'R', 100) , do action UP.
Reach state   ('C', 2, 0, 'D', 100)

From  ('C', 2, 0, 'D', 100) , do action RIGHT.
Reach state   ('E', 2, 0, 'R', 100)

From  ('E', 2, 0, 'R', 100) , do action HIT.
Reach state   ('E', 2, 0, 'R', 50)

From  ('E', 2, 0, 'R', 50) , do action HIT.
Reach state   ('E', 2, 0, 'R', 0)


From our analysis of the policy for the initial state `(W, 0, 0, D, 100)`, we know that hitting with the blade is the best method to kill the Monster in such a situation where the health of Monster is 100. In this the policy for this initial state, that's exactly what's happening. IJ moves to East from Center and HITS monster twice with a blade to reach the final state.

## Task 2

## Case 1

Indiana on the LEFT action at East Square will go to the West Square. 


Between the policies(traces) of Task 1 and Case 1, there are no differences apart from some caused by rounding in state values.

### Policies for given start states

### 1. (W, 0, 0, D, 100)

From  ('W', 0, 0, 'D', 100) , do action RIGHT.
Reach state   ('C', 0, 0, 'D', 100) .

From  ('C', 0, 0, 'D', 100) , do action RIGHT.
Reach state   ('E', 0, 0, 'D', 100) .

From  ('E', 0, 0, 'D', 100) , do action HIT.
Reach state   ('E', 0, 0, 'R', 100) .

From  ('E', 0, 0, 'R', 100) , do action HIT.
Reach state   ('E', 0, 0, 'R', 50) .

From  ('E', 0, 0, 'R', 50) , do action HIT.
Reach state   ('E', 0, 0, 'D', 50) .

From  ('E', 0, 0, 'D', 50) , do action HIT.
Reach state   ('E', 0, 0, 'D', 0) .

### 2. (C, 2, 0, R, 100)

From  ('C', 2, 0, 'R', 100) , do action UP.
Reach state   ('E', 2, 0, 'R', 100) .

From  ('E', 2, 0, 'R', 100) , do action HIT.
Reach state   ('E', 2, 0, 'R', 50) .

From  ('E', 2, 0, 'R', 50) , do action HIT.
Reach state   ('E', 2, 0, 'R', 0) .


## Case 2
The step cost of the STAY action is taken zero.  

Between the policies(traces) of Task 1 and Case 2, we see that action STAY is chosen more number of times as there is no penalty for STAY action in this case.

### Policies for given start states

#### 1. (W, 0, 0, D, 100)

Does not reach end state. 

#### 2. (C, 2, 0, R, 100)

Does not reach end state.


## Case 3
Discount factor gamma = 0.25

### Policies for given start states

#### 1. (W, 0, 0, D, 100)

Does not reach end state.

#### 2. (C, 2, 0, R, 100)

From  ('C', 2, 0, 'R', 100) , do action LEFT.
Reach state   ('E', 2, 0, 'R', 100) .

From  ('E', 2, 0, 'R', 100) , do action LEFT.
Reach state   ('E', 2, 0, 'D', 100) .

From  ('E', 2, 0, 'D', 100) , do action HIT.
Reach state   ('E', 2, 0, 'D', 50) .

From  ('E', 2, 0, 'D', 50) , do action HIT.
Reach state   ('E', 2, 0, 'R', 0) .

## Results obtained in the trace files 
We output the trace of the state, the chosen action at that state and the value of state for all iterations from 0 till convergence in the respective output files for each case.

## Rate of convergence
Task 1 took 125 iterations (0-124).

Task 2 Case 1 took 126 iterations (0-125).

There is little difference between the no. of iterations it took to converge for the case 1 and task 1. The only change that happened in case 1 is that LEFT action from East make IJ go to West instead of Center. But this is a slight change in the state transitions that cannot create significant impact in the number of iterations.


Task 2 Case 2 took 63 iterations (0-62).

When the step cost for the STAY action become zero, IJ can just wait in any cell other than Center and East without incurring any loss (negative reward). So IJ

Task 2 Case 3 took 9 iterations (0-8).

Here, gamma(discount factor) is 0.25. The discount in Task 1 was 0.999. So a significant change happens here because the utility of a state becomes around 25% of what it was before in the next state in case 3. In task 1, there is negligible difference in the utility value of states between consecutive time steps.

Value iteration converges with very less no. of iterations in case 3 because of the small discount factor that makes the value of rewards non-significant after some time steps.

## Cases when end state is not reached

We did not get policy to reach end state in Task 2 Case 2 for the given start states and in Task 2 Case 3 for the first start state.
This situation happens when our policy repeatedly chooses STAY action over other actions. When we do so, we eventually exhaust all the next states we could visit before visiting an end state. Thus we get no policy that can reach an end state from the given start state by only choosing the best actions.

This situation is more probable in Task 2 Case 2 as there is no step cost for STAY action and hence IJ prefers STAY even more than earlier. We can also see that both the given start states result in no policy ending up in an end state in this case.
For Task 2 Case 3, this case occurs only in the first start state.
