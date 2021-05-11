from gurobipy import *

import numpy as np

def eurovision_instance_opt_voting(n, m, prefs, contesters_ids):

    dct = {}
    i = 0

    for id in contesters_ids:
        dct[id] = i
        i += 1

    results = np.ones((m, m))

    for a in contesters_ids:
        for b in contesters_ids:
            if (a == b):
                continue

            model = Model()
            model.setParam('OutputFlag', 0)

            dis = model.addVars(n, n)

            model.addConstrs(dis[i,i] == 0 for i in range(n))
            model.addConstrs((dis[i,j] == dis[j,i] for i in range(n) for j in range(n)))
            model.addConstrs((dis[i,j] <= dis[i,k] + dis[k,j] for i in range(n) for j in range(n) for k in range(n)))

            for i in range(n):
                pref = prefs[i]

                for (k, r) in pref:
                    model.addConstr(dis[i, k] <= dis[i, r])

            model.addConstr(quicksum([dis[i, b] for i in range(n)]) == 1)

            model.setObjective(quicksum([dis[i, a] for i in range(n)]), GRB.MAXIMIZE)

            # solve model
            model.optimize()

            if model.status == GRB.OPTIMAL:
                #print('Optimal objective: %g' % model.objVal)
                results[dct[a]][dct[b]] = model.objVal
            elif model.status == GRB.UNBOUNDED or model.status == GRB.INF_OR_UNBD:
                print('Model is unbounded')
                results[dct[a]][dct[b]] = float("inf")
            else:
                print('Optimization ended with status %d' % model.status)

    distortions = np.max(results, axis=1)
    return distortions

# display solution
#if model.SolCount > 0:
  #model.printAttr('dis')

# export model
#model.write('knapsack.lp')
