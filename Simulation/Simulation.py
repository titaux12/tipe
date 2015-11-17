# coding: utf8

from Route import *


class Simulation(object):

    def __init__(self):
        self.temps = 5*60.0 # Durée de la simulation en secondes
        self.delta = 1/15.0 # Intervalle de temps entre chaque calcul
        self.route = Route()

    def parametres(self):
        pass

    def initialisation(self):
        self.route.initialisation(self.delta)

    def lancer(self):
        self.initialisation()

        temps_total = 0
        p = 0
        i = 0
        indice = 0
        while temps_total <= self.temps:
            self.route.update(self.delta, temps_total, indice)
            indice += 1
            temps_total += self.delta
            i += self.delta / self.temps
            if i >= 0.01:
                p += 0.01
                i -= 0.01
                print("Avancement de la simulation : " + str(round(p*100)) + "%")
        print("Fin de la simulation")

        self.route.analyse_voitures()
        self.route.animation()
        self.route.analyse_trafic()

        print("Arrêt de la simulation")

s = Simulation()
s.lancer()
