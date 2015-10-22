# coding: utf8

from Route import *


class Simulation(object):

    def __init__(self):
        self.temps = 5*60.0 # Durée de la simulation en secondes
        self.delta = 1/30.0 # Intervalle de temps entre chaque calcul
        self.route = Route()

    def parametres(self):
        pass

    def initialisation(self):
        self.route.initialisation()

    def lancer(self):
        self.initialisation()

        temps_total = 0
        p = 0
        i = 0
        while temps_total <= self.temps:
            self.route.update(self.delta, temps_total)
            temps_total += self.delta
            i += self.delta / self.temps
            if i >= 0.1:
                p += i
                i -= 0.1
                print("Avancement de la simulation : " + str(round(p*100)) + "%")
        print("Fin de la simulation")

        # self.route.analyse_voitures()
        self.route.analyse_trafic()

        print("Arrêt de la simulation")

s = Simulation()
s.lancer()
