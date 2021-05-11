from gurobipy import *

import numpy as np


def instance_opt_decisive_voting(n, m, prefs, alpha=1):
    results = np.ones((m, m))

    for a in range(m):
        for b in range(m):
            if (a == b):
                continue

            model = Model()
            model.setParam('OutputFlag', 0)

            dis = model.addVars(n+m, n+m)

            model.addConstrs(dis[i,i] == 0 for i in range(n+m))
            model.addConstrs((dis[i,j] == dis[j,i] for i in range(n+m) for j in range(n+m)))
            model.addConstrs((dis[i,j] <= dis[i,k] + dis[k,j] for i in range(n+m) for j in range(n+m) for k in range(n+m)))

            for i in range(n):
                pref = prefs[i]

                k, r = pref[0]

                model.addConstr(dis[i, n+k] <= alpha*dis[i, n+r])

                for (k, r) in pref:
                    model.addConstr(dis[i, n+k] <= dis[i, n+r])

            model.addConstr(quicksum([dis[i, n+b] for i in range(n)]) == 1)

            model.setObjective(quicksum([dis[i, n+a] for i in range(n)]), GRB.MAXIMIZE)

            # solve model
            model.optimize()

            if model.status == GRB.OPTIMAL:
                #print('Optimal objective: %g' % model.objVal)
                results[a][b] = model.objVal

                #for v in model.getVars():
            #        print('%s %g' % (v.varName, v.x))

            elif model.status == GRB.UNBOUNDED or model.status == GRB.INF_OR_UNBD:
                print('Model is unbounded')
                results[a][b] = float("inf")
            else:
                print('Optimization ended with status %d' % model.status)

    costs = np.max(results, axis=1)
    return costs

# display solution
#if model.SolCount > 0:
  #model.printAttr('dis')

# export model
#model.write('knapsack.lp')
