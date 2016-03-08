# coding: utf8

import pickle
import os
from pylab import *

"""
Analyse du flux et de la densité des différentes simulations à partir des résultats stockés dans le dossier 'Données'
"""

F, D, V = [], [], []

fichiers = os.listdir(os.getcwd() + "/Simulation/Données/")
l = len(fichiers)
if l > 0:
    c = 0
    for nom_fichier in fichiers:
        c += 1
        print(c/l*100, "%")
        with open(os.getcwd() + "/Simulation/Données/" + nom_fichier, 'rb') as fichier:
            p = pickle.Unpickler(fichier)
            params = p.load()
            # print(params)

            flux_total = p.load()
            densite_totale = p.load()

            vitesse = p.load()

            # On ajoute uniquement la dernière donnée celle qui correspond à un regime stationnaire
            F.append(flux_total[len(flux_total) - 1][1])
            D.append(densite_totale[len(densite_totale) - 1][1])
            V.append(vitesse)

    plot(D, F, 'bo')
    xlim(0, max(D) * 1.2)
    ylim(0, max(F) * 1.2)
    show()

    plot(V, F, 'bo')
    xlim(0, max(V) * 1.2)
    ylim(0, max(F) * 1.2)
    show()

else:
    print("Aucune donnée à traiter !")
