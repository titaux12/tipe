# coding: utf8

from Simulation import Simulation
from math import exp
import cProfile

fct="x"

def gaussienne(x):
    return 0.06*(exp(-0.00001*(x-500)**2)*0.5 + 0.1)

def fonction(x):
    return eval(fct)

def feux_rouges(x):
    if x <= 1000:
        return 0.07
    else:
        return 0


def constante(x):
    return 0.02

for y in range(1,100):
    fct="0.06*(exp(-0.00001*(x-500)**2/y)*0.5 + 0.1)"
    s = Simulation(600, 1/20.0)
    s.route.ajouter_section(2000, 25)
    s.initialisation(fonction)
    s.route.boucle = True
    s.sauvegarde = False
    s.lancer()

s = Simulation(600, 1/20.0)
s.route.ajouter_section(2000, 25)

s.initialisation(gaussienne)
# s.analyse = True
# s.route.desactiver_densite()
# s.route.desactiver_flux()
s.route.boucle = True
s.sauvegarde = False

# cProfile.run('s.lancer()')
s.lancer()
