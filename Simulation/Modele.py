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

<<<<<<< HEAD:Simulation/Modele.py
    def calcul_force(self, voiture, Dx, Dv, vitesse_limite):
        """
        :return: L'accélération du véhicule en fonction du véhicule de devant
        """
        # Détermination du régime via le calcul du temps relatif
        Dt = self.temps_max + 1
        v = voiture.vitesse
        if v != 0:
            Dt = Dx / v

        F_max = voiture.F_max
        F_min = voiture.F_min
        v_max = vitesse_limite
        l = voiture.longueur

        if Dt >= self.temps_max: # Régime libre
            if v < v_max:
                return F_max
            elif v == v_max:
                return 0
            else:
                return -F_min
        elif Dt >= self.temps_min: # Régime contraint par la voiture de devant
            return self.alpha * v**self.beta * (Dv / (Dx - l)**self.gamma)
        else: # Régime de freinage d'urgence
            return -F_min
=======
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
>>>>>>> axelsauvage/master:Modele.py
