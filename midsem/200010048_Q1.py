# %% [markdown]
# # Imports

# %%
import random
import gurobipy as gp
from gurobipy import GRB, quicksum, max_
import matplotlib.pyplot as plt
from time import time
# %% [markdown]
# # Utils

# %%
def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def distance_matrix_generator(switch_positions):
    # N: Number of switches
    # scale: Extent of Distance
    N = len(switch_positions)
    graph = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            weight = distance(switch_positions[i], switch_positions[j])
            graph[i][j] = weight
            graph[j][i] = weight
    return graph

# %% [markdown]
# # Inputs

# %%
# Speed is not Required as time is proportional to distance
NUM_CONTROLLERS = 10
NUM_SWITCHES = 100
PACKET_IN = 10
CONTROL_CAP = 100
SCALE = 500
switch_positions = [(random.randint(0, SCALE), random.randint(0, SCALE)) for _ in range(NUM_SWITCHES)]
distance_matrix = distance_matrix_generator(switch_positions)
print(f"Data Created with {NUM_SWITCHES} switches")
print(f"Capacity of each switch: {CONTROL_CAP}")
print(f"Packet In Rate: {PACKET_IN}")

# %% [markdown]
# # Create Model

# %%
model = gp.Model("Controller_Placement")
print("Model Created")

## I am Assuming that controllers are associated with a switch and not in a random location.

# Is there a controller associated with the switch
associate_controller  = {}
for sw in range(NUM_SWITCHES):
    associate_controller[sw] = model.addVar(vtype=GRB.BINARY, name=f'ac_{sw}')
                                     
# Switch Controller Mapping
sw_cont_mapping = {}
for sw in range(NUM_SWITCHES):
    for con in range(NUM_SWITCHES):
        sw_cont_mapping[sw, con] = model.addVar(vtype=GRB.BINARY, name=f'map_{sw}_{con}')
    
print(f"Decision Variables Created")

# %% [markdown]
# # Constraints

# %% [markdown]
# ### 1. Capacity Constraint

# %%
for con in range(NUM_SWITCHES):
    model.addConstr(quicksum(
                        PACKET_IN*sw_cont_mapping[sw, con]
                        for sw in range(NUM_SWITCHES)
                    ) <= CONTROL_CAP*associate_controller[con],
                    name=f'1_{con}')

# %% [markdown]
# ### 2. Each switch must have a controller

# %%
for sw in range(NUM_SWITCHES):
    model.addConstr(quicksum(
                        sw_cont_mapping[sw, con]
                        for con in range(NUM_SWITCHES)
                    ) == 1,
                    name=f'2_{sw}')

# %% [markdown]
# ### 3. If a switch is associated with a controller then it is mapped to the contoller

# %%
for con in range(NUM_SWITCHES):
    model.addConstr( sw_cont_mapping[con, con] == associate_controller[con],
                    name=f'3_{con}')

# %% [markdown]
# ### 4. Fix the number of controllers

# %%
model.addConstr( quicksum(
                    associate_controller[con]
                    for con in range(NUM_SWITCHES)
                    ) == NUM_CONTROLLERS, 
                name=f'4_{con}')

# %% [markdown]
# # Objective

# %%
# Minimize the CC distance and CS distance

cc_distance = quicksum(
                associate_controller[sw]*associate_controller[con]*distance_matrix[sw][con]
                for sw in range(NUM_SWITCHES)
                for con in range(NUM_SWITCHES)
            )

sc_distance = quicksum(
                distance_matrix[sw][con]*sw_cont_mapping[sw, con]
                for sw in range(NUM_SWITCHES)
                for con in range(NUM_SWITCHES)
            )

model.setObjective( 0.05*cc_distance + sc_distance, GRB.MINIMIZE)

# %% [markdown]
# # Optimization

# %%
start_time = time()
max_time = 5*60 # 5 minutes

# Terminate the model after 5 minutes
def model_callback(model, where):
    if max_time < time() - start_time:
        model.terminate()

model.optimize(callback=model_callback)

# %% [markdown]
# # Analysis

# %%
con_sw_map = dict()

for sw in range(NUM_SWITCHES):
    for con in range(NUM_SWITCHES):
        if sw_cont_mapping[sw, con].x == 1:
            if con not in con_sw_map:
                con_sw_map[con] = []
            con_sw_map[con].append(sw)

print(f"Objective Value: {model.objVal}")
con_sw_map

# %%
X = [switch_positions[i][0] for i in range(NUM_SWITCHES)]
Y = [switch_positions[i][1] for i in range(NUM_SWITCHES)]
color = ['red' if i in con_sw_map else 'blue' for i in range(NUM_SWITCHES)]

plt.figure(figsize=(8, 8))
plt.title("Switch Controller Plot")
plt.scatter(X, Y, c=color, s=40)

# %%



