# coding: utf8

from pylab import *

"""
Présentation du modèle :
Il y a 3 types de régimes:
    - Régime libre: la voiture tend à rouler à la vitesse maximale
    - Régime contraint: la voiture adapte son allure en fonction de la voiture de devant
    - Régime freinage d'urgence: la voiture est beaucoup trop proche et freine au maximum
Le régime est déterminé en fonction du temps relatif:
    - Régime libre si Dt >= temps_max en général dans les 10 secondes
    - Régime contraint si temps_min <= Dt <= temps_max ou temps_min est le temps de sécurité soit 2 secondes en général
    - Régime d'urgence si Dt <= temps_min
De plus, 3 coefficients permettent d'influencer les paramètres:
    - alpha: coefficient global
    - beta: influence de la vitesse du véhicule dans la réaction
    - gamma: influence de la distance
"""


class Modele(object):

    def __init__(self, parametres):
        self.temps_max = parametres[0]
        self.temps_min = parametres[1]
        self.alpha = parametres[2]
        self.beta = parametres[3]
        self.gamma = parametres[4]

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
