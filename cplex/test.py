#仮想環境入るもよし、$py -3.8 test.pyもよし(macの検証はこれから)
import cplex

var = ['x', 'y'] # variables
b = [20, 30] # objective function
c = [800, 1800, 1500] # constraints
A = [
      [var, [1, 2]],
      [var, [3, 4]],
      [var, [3, 1]],
    ]

prob = cplex.Cplex()
prob.objective.set_sense(prob.objective.sense.maximize) # maximization problem
prob.variables.add(obj=b, names=var)
prob.linear_constraints.add(lin_expr=A, senses=['L']*3, rhs=c)
prob.solve()

x = prob.solution.get_values()

for i in range(len(var)):
    print("{} = {}".format(var[i], x[i]))
print(prob.solution.get_objective_value())