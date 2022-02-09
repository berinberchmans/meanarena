import mdptoolbox
import numpy as np
import csv



# The MDP Toolbox defines MDPs through a probability array and a reward array.

# 

# The probability array has shape (A, S, S), where A are actions and S
# are states. So A arrays, each S x S, ie for each action specify the
# transitions probabilities of reaching the second state by applying
# that action in the first state.

# So, to implement the action model described above, we need:
P1 = np.array([[[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]],
               [[0.2, 0.8, 0,   0],
                [0,   0.2, 0.8, 0],
                [0,   0,   0.2, 0.8],
                [0,   0,   0,   1]]])
# The first matrix is that for the action "Stay" (when executed in a given
# state the agent stays there) and the second is for the action "Right" 
# (which shifts the agent right with probability 0.8 except in state 3 
# when the agent remains in state 3 with probability 1).

# The reward array has shape (S, A), so there is a set of S vectors,
# one for each state, and each is a vector with one element for each 
# the actions --- each element is the reward for executing the relevant 
# action in the state (so this is really modelling cost of the action).
R1 = np.array([[-0.04, -0.04], [-0.04, -0.04], [-0.04, -0.04], [1, 1]])
# R1 says that executing either action in states 0, 1, or 2 has a reward
# of -0.04, and executing either action in state 3 has reward 1.

# The util.check() function checks that the reward and probability matrices 
# are well-formed, and match.
# 
# Success is silent, failure provides somewhat useful error messages.
mdptoolbox.util.check(P1, R1)
# To run value iteration we create a value iteration object, and run it. Note that 
# discount value is 0.9
vi1 = mdptoolbox.mdp.ValueIteration(P1, R1, 0.9)
vi1.run()
# We can then display the values (utilities) computed, and look at the policy:
print('Values:\n', vi1.V)
print('Policy:\n', vi1.policy)
cost = -0.04
R3 = np.array([[cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [-1,    -1,    -1,    -1,  ],
               [cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [cost,  cost,  cost, cost],
               [1,      1,     1,     1,  ]])
P3 = np.array([[[0.1, 0.8, 0,   0,   0.1, 0,   0,   0,   0,   0,   0  ], # Right, State 0
                [0,   0.2, 0.8, 0,   0,   0,   0,   0,   0,   0,   0  ],
                [0,   0,   0.1, 0.8, 0,   0.1, 0,   0,   0,   0,   0  ],
                [0,   0,   0,   0.9, 0,   0,   0.1, 0,   0,   0,   0  ],
                [0.1, 0,   0,   0,   0.8, 0,   0,   0.1, 0,   0,   0  ],
                [0,   0,   0.1, 0,   0,   0,   0.8, 0,   0,   0.1, 0  ],
                [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0  ], # State 6 is absorbing
                [0,   0,   0,   0,   0.1, 0,   0,   0.1, 0.8, 0,   0  ],
                [0,   0,   0,   0,   0,   0,   0,   0,   0.2, 0.8, 0  ],
                [0,   0,   0,   0,   0,   0.1, 0,   0,   0,   0.1, 0.8],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1  ]],# State 10 is absorbing
               [[0.9, 0,   0,   0,   0.1, 0,   0,   0,   0,   0,   0  ], # Left
                [0.8, 0.2, 0,   0,   0,   0,   0,   0,   0,   0,   0  ],
                [0,   0.8, 0.1, 0,   0,   0.1, 0,   0,   0,   0,   0  ],
                [0,   0,   0.8, 0.1, 0,   0,   0.1, 0,   0,   0,   0  ],
                [0.1, 0,   0,   0,   0.8, 0,   0,   0.1, 0,   0,   0  ],
                [0,   0,   0.1, 0,   0,   0.8, 0.1, 0,   0,   0,   0  ],
                [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0  ],
                [0,   0,   0,   0,   0.1, 0,   0,   0.9, 0,   0,   0  ],
                [0,   0,   0,   0,   0,   0,   0,   0.8, 0.2, 0,   0  ],
                [0,   0,   0,   0,   0,   0.1, 0,   0,   0.8, 0.1, 0  ],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1  ]], 
               [[0.1, 0.1, 0,   0,   0.8, 0,   0,   0,   0,   0,   0  ], # Up
                [0.1, 0.8, 0.1, 0,   0,   0,   0,   0,   0,   0,   0  ],
                [0,   0.1, 0,   0.1, 0,   0.8, 0,   0,   0,   0,   0  ],
                [0,   0,   0.1, 0.1, 0,   0,   0.8, 0,   0,   0,   0  ],
                [0,   0,   0,   0,   0.2, 0,   0,   0.8, 0,   0,   0  ],
                [0,   0,   0,   0,   0,   0.1, 0.1, 0,   0,   0.8, 0  ],
                [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0  ],
                [0,   0,   0,   0,   0,   0,   0,   0.9, 0.1, 0,   0  ],
                [0,   0,   0,   0,   0,   0,   0,   0.1, 0.8, 0.1, 0  ],
                [0,   0,   0,   0,   0,   0,   0,   0,   0.1, 0.8, 0.1],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1  ]],
               [[0.9, 0.1, 0,   0,   0,   0,   0,   0,   0,   0,   0  ], # Down
                [0.1, 0.8, 0.1, 0,   0,   0,   0,   0,   0,   0,   0  ],
                [0,   0.1, 0.8, 0.1, 0,   0,   0,   0,   0,   0,   0  ],
                [0,   0,   0.1, 0.9, 0,   0,   0,   0,   0,   0,   0  ],
                [0.8, 0,   0,   0,   0.2, 0,   0,   0,   0,   0,   0  ],
                [0,   0,   0.8, 0,   0,   0.1, 0.1, 0,   0,   0,   0  ],
                [0,   0,   0,   0,   0,   0,   1,   0,   0,   0,   0  ],
                [0,   0,   0,   0,   0.8, 0,   0,   0.1, 0.1, 0,   0  ],
                [0,   0,   0,   0,   0,   0,   0,   0.1, 0.8, 0.1, 0  ],
                [0,   0,   0,   0,   0,   0.8, 0,   0,   0.1, 0,   0.1],
                [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1  ]]])

mdptoolbox.util.check(P3, R3)

vi2 = mdptoolbox.mdp.ValueIteration(P3, R3, 0.9)
vi2.run()

print('Values:\n', vi2.V)
print('Policy:\n', vi2.policy)

    # f = open('D:/Uni projects/AI/git/meanArena/ztemptext.csv', 'a')
        # writer = csv.writer(f)
        # cccc = finaldd2
        # for ynt in range(worldBreadth):
        #     for xnt in range(worldLength):
        #         if(ynt == oy and xnt == ox ):
        #             cccc[ynt][xnt] =666
        #     writer.writerow(cccc[ynt])
        # writer.writerow("################################")
        # f.close()
        

                   
        # Policy movement
        # if(themove == 0):
        #     print("Right")
        #     return Directions.EAST
        # elif(themove == 1):
        #     print("Left")
        #     return Directions.WEST
        # elif(themove == 2):
        #     print("Up")
        #     return Directions.SOUTH
        # elif(themove == 3):
        #     print("Down")
        #     return Directions.NORTH
        
themove = finaldd[myPosition.x][(worldBreadth-1)-myPosition.y]


This is a solution that works, however only efficiently in case of arenas with limited sizes, as with the increase in size and decrease in visibility limit will require Tallon to waste time searching. However, for the scope of this game, the method works as it doesn’t require extremely large arenas..