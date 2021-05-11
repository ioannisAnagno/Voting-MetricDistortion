from instance_opt import instance_opt_voting
import numpy as np
from numpy.random import permutation

import matplotlib.pyplot as plt

plt.style.use('ggplot')

n = 50 # Number of voters

m = 6 # Number of candidates

num_iter = 5 # Number of random realizations

y_axis = [[] for i in range(num_iter)]

for it in range(num_iter):

    ps = []

    for i in range(n):
        p = permutation([i for i in range(m)]) # A (uniformly) random permutation
        ps.append(p)

    '''
        Only an eps fraction of voters provide information
    '''

    for eps in [0.2, 0.4, 0.6, 0.8, 1]:

        prefs = []

        for i in range(n):
            if (i >= eps*n):
                prefs.append([])
                continue
            p = ps[i]
            pref = []
            for j in range(m+1):
                for r in range(j+1, m):
                    pref.append((p[j], p[r]))

            prefs.append(pref)

        # Determine the distortion of every candidate
        distortions = instance_opt_voting(n, m, prefs)

        print(min(distortions))

        y_axis[it].append(min(distortions))
        
plt.rcParams.update({'font.size': 16})
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

x_axis = [0.2, 0.4, 0.6, 0.8, 1]

colors = ['crimson', 'darkblue', 'green', 'k', 'goldenrod']

for it in range(num_iter):

    plt.plot(x_axis, y_axis[it], '.', c=colors[it], markersize=7)
    plt.plot(x_axis, y_axis[it], '-', c=colors[it], linewidth=0.8)

    upper_y = np.array(y_axis[it]) + 0.2
    lower_y = np.array(y_axis[it]) - 0.2
    plt.fill_between(x_axis, upper_y, lower_y, alpha = .1, color = 'darkorchid')

plt.xticks(x_axis, ['20\%', '40\%', '60\%', '80\%', '100\%'])
plt.xlabel('$1 - \epsilon$')
plt.ylabel('Distortion')
plt.show()
