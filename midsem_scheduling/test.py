import gurobipy as gp
from gurobipy import GRB

# Create a Gurobi model
model = gp.Model("ApproximateOnesConstraint")

# Define the dimensions of the matrix
m = 5  # Replace with your desired number of rows
n = 6  # Replace with your desired number of columns
target_ones = n  # The desired number of ones (approximately)

# Create binary decision variables for the matrix elements
X = {}
for i in range(m):
    for j in range(n):
        X[i, j] = model.addVar(vtype=GRB.BINARY, name=f'X_{i}_{j}')

# Create binary variables to track rows with at least one '1'
Y = {}
for i in range(m):
    Y[i] = model.addVar(vtype=GRB.BINARY, name=f'Y_{i}')

# Constraint to ensure approximately n ones in the matrix
model.addConstr(gp.quicksum(X[i, j] for i in range(m) for j in range(n)) == target_ones, "Approximate_Ones")

# Constraints to link Y[i] to the presence of '1's in row i
for i in range(m):
    model.addConstr(Y[i] >= gp.quicksum(X[i, j] for j in range(n)), f'AtLeastOne_1_{i}')
    model.addConstr(Y[i] <= gp.quicksum(X[i, j] for j in range(n)), f'AtLeastOne_2_{i}')

# Minimize the sum of Y values to minimize the number of rows with at least one '1'
model.setObjective(gp.quicksum(Y[i] for i in range(m)), GRB.MINIMIZE)

# Optimize the model
model.optimize()

# Print the solution
if model.status == GRB.OPTIMAL:
    print("Optimal solution found.")
    for i in range(m):
        print(f"Row {i}: Y_{i} = {Y[i].X}")
else:
    print("No optimal solution found.")
