# coding: utf8

import pickle
import os
from pylab import *

"""
Analyse du flux et de la densité des différentes simulations
"""

X, Y = [], []

fichiers = os.listdir(os.getcwd() + "/Simulation/Données/")
print(fichiers)
for nom_fichier in fichiers:
    with open(os.getcwd() + "/Simulation/Données/" + nom_fichier, 'rb') as fichier:
        p = pickle.Unpickler(fichier)
        params = p.load()
        print(params)
        flux_total = p.load()
        densite_totale = p.load()

        # for d in flux_total:
        #     Y.append(d[1])
        # for d in densite_totale:
        #     X.append(d[1])

        Y.append(flux_total[len(flux_total)-1][1])
        X.append(densite_totale[len(densite_totale)-1][1])

# hist2d(np.array(X), np.array(Y), cmap="afmhot", bins=60)
plot(X, Y, 'bo')
xlim(0, max(X)*1.2)
ylim(0, max(Y)*1.2)
show()