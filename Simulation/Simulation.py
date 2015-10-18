# coding: utf8

from Route import *

class Simulation(object):

    temps = 10.0*60.0 # Durée de la simulation en secondes
    delta = 1/60.0 # Intervalle de temps entre chaque calcul

    def __init__(self):
        pass

    def parametres(self):
        pass

    def initialisation(self):
        self.route = Route()
        self.route.initialisation()

    def lancer(self):
        self.initialisation()

        temps_total = 0
        while temps_total < self.temps:
            temps_total += self.delta
            self.route.update(self.delta, temps_total)

        self.route.afficher_graphique()

s = Simulation()
s.lancer()