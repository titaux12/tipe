# coding: utf8

from random import uniform
import numpy as np
from Modele import *

class Voiture(object):

    def __init__(self, position, vitesse):
        assert position >= 0
        assert vitesse >= 0
        self.donnees = [] # Tableau contenant les données enregistrées lors de la simulation
        #                   = [temps_total, [self.position,self.vitesse,G], indice]
        self.position = position # position en mètre
        self.vitesse = vitesse # vitesse en m/s

        self.indice_section=0
        self.masse = 1300 # masse en kg
        self.longueur = 4 # longueur en mètre
        self.F_max = 10000 # Force d'accélération maximum en newton
        self.F_min = 10000 # Force de freinage maximum en newton
        self.valide = True # Booléen pour savoir si la voiture doit être prise en compte dans la simulation
        self.coefficient_vitesse = uniform(0.95, 1.05) #Pourcentage de la vitesse limité adopté.

        self.temps_reaction = 2 # Temps de réaction du conducteur en secondes
        # Création du modèle pour la gestion de l'accélération
        self.modele = Modele(2)

    def update(self, temps_total, delta, indice, voiture_devant, longueur, temps_securite, vitesse_limite, boucle=True):
        vitesse_limite *= self.coefficient_vitesse
        if self.position >= longueur:
            if boucle: # Si on boucle on soustrait la longueur de la route à la position de la voiture
                self.position -= longueur
            else: # Sinon on retire la voiture de la simulation
                self.valide = False
                
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

            distance_securite = temps_securite * (2*self.vitesse - v)
            delta_v = v - self.vitesse # Vitesse relative
            # Distance relative
            if self.position <= p:
                delta_x = p - self.position
            else:
                delta_x = longueur - abs(p - self.position)
        else:
            delta_x = 1000000
            delta_v = -1000000

        self.modele.temps_securite = temps_securite # Mise à jour du temps de sécurité

        # Calcul de la force appliquée par le conducteur
        F = self.modele.calcul_force(self.vitesse, delta_x, vitesse_limite)

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

    def tours_max(self):
        tours=0
        for i in range(len(self.donnees)):
            pass
    
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
