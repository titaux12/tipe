# coding: utf8

from random import uniform
import numpy as np
from Modele import Modele

class Voiture(object):

    def __init__(self, position, vitesse, vitesse_limite):
        assert position >= 0
        assert vitesse >= 0
<<<<<<< HEAD
        # Vitesse et position initiales de la voiture
        self.position = position # position en mètre
        self.vitesse = vitesse # vitesse en m/s

        self.indice_section=0
        self.donnees = [] #=[temps_total, [self.position,self.vitesse,G], indice]
        self.masse = 1300 # masse en kg
        self.longueur = 4 # longueur en mètre
        self.F_max = 5000 # Force d'accélération maximum
        self.F_min = 10000 # Force de freinage maximum
        self.valide = True # False si la voiture est arrivée à la fin de la route
        self.coefficient_vitesse = uniform(0.95, 1.05)
        self.temps_reaction = 2 # Temps de réaction du conducteur

    def update(self, temps_total, delta, indice, voiture_devant, longueur, temps_securite, vitesse_limite):
        vitesse_limite = vitesse_limite * self.coefficient_vitesse
        if self.position >= longueur:
            # self.valide = False
            self.position -= longueur
        else:
            # Influence de la voiture de devant
            if voiture_devant is not None:

                indice_decalage = indice - round(self.temps_reaction / delta)
                v = voiture_devant.obtenir_vitesse(indice_decalage)
                p = voiture_devant.obtenir_position(indice_decalage)
                if v is None:
                    v = voiture_devant.vitesse
                if p is None:
                    p = voiture_devant.position

                distance_securite = temps_securite * (2*self.vitesse - v)
                # Distance relative par rapport à la voiture de devant
                #C'est plus la distance qui sépare la voiture de la distance de sécurité
                if self.position <= p:
                    delta_h = abs(p - self.position) - distance_securite
                else:
                    delta_h = longueur - abs(p - self.position) - distance_securite
            else:
                delta_h = 10000

            # Calcul de la force appliquée par le conducteur
            G = self.force(delta_h)
            n = self.F_max / vitesse_limite

            if G > 0:
                G *= self.F_max
=======

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

    def update(self, temps_total, delta, indice, voiture_devant, longueur, boucle=True):
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

            delta_v = v - self.vitesse # Vitesse relative
            # Distance relative
            if self.position <= p:
                delta_x = p - self.position
>>>>>>> axelsauvage/master
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
