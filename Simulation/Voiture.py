# coding: utf8

from random import uniform
import numpy as np
from Modele import Modele

class Voiture(object):

    def __init__(self, position, vitesse, vitesse_limite):
        assert position >= 0
        assert vitesse >= 0

        self.donnees = [] # Tableau contenant les données enregistrées lors de la simulation
        self.position = position # Position en mètre
        self.vitesse = vitesse # Vitesse en m/s
        self.masse = 1300 # Masse en kg
        self.longueur = 4 # Longueur en mètre
        self.F_max = 1500 # Force d'accélération maximum en newton
        self.F_min = 3000 # Force de freinage maximum en newton
        self.valide = True # Booléen pour savoir si la voiture doit être prise en compte dans la simulation
        self.vitesse_limite = vitesse_limite # Vitesse limite du conducteur en m/s
        self.temps_reaction = 2 # Temps de réaction du conducteur en secondes
        # Création du modèle pour la gestion de l'accélération
        self.modele = Modele(
            [8, 2, 1, 2, 0.5]
        )

    def update(self, temps_total, delta, indice, voiture_devant, longueur):
        if self.position >= longueur:
            # self.valide = False
            self.position -= longueur

        # Influence de la voiture de devant
        if voiture_devant is not None:
            """ Intégration du temps de réaction """
            indice_decalage = indice - round(self.temps_reaction / delta)
            v = voiture_devant.obtenir_vitesse(indice_decalage)
            p = voiture_devant.obtenir_position(indice_decalage)
            if v is None:
                v = voiture_devant.vitesse
            if p is None:
                p = voiture_devant.position

            delta_v = v - self.vitesse # Vitesse relative
            # Distance relative
            if self.position <= p:
                delta_x = p - self.position
            else:
                delta_x = longueur - abs(p - self.position)
        else:
            delta_x = 1000000
            delta_v = -1000000

        # Calcul de la force appliquée par le conducteur
        F = self.modele.calcul_force(self, delta_x, delta_v)

        # On limite la force appliquée par le conducteur
        F = min(F, self.F_max)
        F = max(F, -self.F_min)

        # Calcul de l'accélération via le PFD
        a = F / self.masse

        # Intégration d'Euler
        self.vitesse += a * delta
        if self.vitesse < 0: # Impossible de reculer
            self.vitesse = 0
        self.position += self.vitesse * delta

        # Enregistrement des données
        self.donnees.append([
            temps_total,
            [
                self.position,
                self.vitesse,
                F
            ],
            indice
        ])

    def obtenir_positions(self, temps=True):
        if temps:
            t = []
            r = []
            for d in self.donnees:
                t.append(d[0])
                r.append(d[1][0])
            return t, r
        else:
            i = []
            r = []
            for d in self.donnees:
                i.append(d[2])
                r.append(d[1][0])
            return i, r

    def obtenir_vitesse(self, i):
        for d in self.donnees:
            if d[2] == i:
                return d[1][1]
        return None

    def obtenir_position(self, i):
        for d in self.donnees:
            if d[2] == i:
                return d[1][0]
        return None

    def obtenir_vitesses(self):
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][1])
        return t, r

    def obtenir_forces(self):
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][2])
        return t, r
