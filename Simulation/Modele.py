# coding: utf8

from pylab import *

"""
Présentation du modèle :
On calcule une vitesse optimale à adopter par le conducteur qui est fonction de la distance relative
On applique ensuite une force proportionnelle à la différence entre cette vitesse optimale et la vitesse du véhicule
"""


class Modele(object):

    def __init__(self, temps_securite):
        self.temps_securite = temps_securite

    def calcul_force(self, vitesse, Dx, v_max):
        """
        :return: L'accélération du véhicule en fonction du véhicule de devant
        """
        v_o = self.vitesse_optimale(Dx, v_max, vitesse)
        return 700 * (v_o - vitesse)

    def vitesse_optimale(self, Dx, v_max, v):
        return (arctan(0.1 * (Dx - self.temps_securite * v))/pi + 0.5) * v_max

def tracer():
    v_max = 36

    X = linspace(0, 300)
    V = []
    for x in X:
        v_o = (arctan(0.1*(x - 2*v_max))/pi + 0.5) * v_max
        V.append(v_o)
    plot(X, V)
    show()

if __name__ == '__main__':
    tracer()

