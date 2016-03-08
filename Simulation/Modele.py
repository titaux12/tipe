# coding: utf8

from pylab import *

"""
Présentation du modèle :
L'objectif de ce modèle est de déterminer l'accélération du véhicule en fonction des différents paramètres
qui lui sont accessibles: sa vitesse, la vitesse de la voiture de devant et la distance la séparant à cette dernière.
Le conducteur doit respecter une distance minimale de sécurité avec la voiture de devant ainsi que la limitation
de vitesse de la section de route traversée.
"""


class Modele(object):

    def __init__(self, a_max, a_min, temps_reaction, longueur):
        """
        Initialisation des paramètres du modèle
        :param a_max: accélération maximale de la voiture
        :param a_max: décélération maximale de la voiture
        :param temps_reaction: temps de réaction du conducteur en secondes
        :param longueur: longueur de la voiture
        """
        self.a_max = a_max
        self.a_min = a_min
        self.temps_reaction = temps_reaction
        self.longueur = longueur

    def calcul_acceleration(self, v_j, v_i, distance, vitesse_limite):
        """
        :param v_j: la vitesse de la voiture de devant
        :param v_i: la vitesse de la voiture
        :param distance: la distance entre la voiture et celle de devant
        :param vitesse_limite: vitesse_maximale autorisée sur la section de route
        :return: L'accélération du véhicule
        """

        # Calcul du temps de sécurité
        temps_securite = 3 * vitesse_limite / self.a_min + self.temps_reaction

        distance_securite = temps_securite * v_i + self.longueur  # Distance à respecter avec le véhicule de devant
        delta_x = distance_securite - distance

        if delta_x < 0:  # Si la distance de sécurité est respectée, on cherche à aller le plus vite possible
            vitesse_desiree = vitesse_limite
        else:  # Sinon on adopte une vitesse plus faible que celle de devant
            vitesse_desiree = v_j * (1 - delta_x / distance_securite)

        if vitesse_desiree > vitesse_limite:  # On majore la vitesse désirée par la vitesse limite
            vitesse_desiree = vitesse_limite
        if vitesse_desiree < 0:
            vitesse_desiree = 0

        # Pour éviter les problèmes de division par 0
        vitesse_desiree += 0.0000001

        return self.a_max * (1 - v_i / vitesse_desiree)
