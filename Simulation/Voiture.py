# coding: utf8

from random import uniform
import numpy as np

class Voiture(object):

    def __init__(self, position, vitesse, vitesse_limite):
        assert position >= 0
        assert vitesse >= 0
        # Vitesse et position initiales de la voiture
        self.position = position # position en mètre
        self.vitesse = vitesse # vitesse en m/s

        self.donnees = []
        self.masse = 1300 # masse en kg
        self.longueur = 4 # longueur en mètre
        self.F_max = 5000 # Force d'accélération maximum
        self.F_min = 10000 # Force de freinage maximum
        self.valide = True # False si la voiture est arrivée à la fin de la route
        self.vitesse_limite = vitesse_limite * uniform(0.95, 1.05)
        self.temps_reaction = 2 # Temps de réaction du conducteur
        self.temps_securite = 2

    def update(self, temps_total, delta, indice, voiture_devant, longueur):
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

                distance_securite = 2 * (2*self.vitesse - v) #A revoir la formule (je ne comprend pas la place des 2)
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
            n = self.F_max / self.vitesse_limite

            if G > 0:
                G *= self.F_max
            else:
                G *= self.F_min

            F = G - n * self.vitesse

            F = min(F, self.F_max)
            F = max(F, -self.F_min)

            # Calcul de l'accélération via le PFD
            a = F / self.masse

            # Intégration d'Euler
            self.vitesse += a * delta
            if self.vitesse < 0:
                self.vitesse = 0
            self.position += self.vitesse * delta

            # Enregistrement des données
            self.donnees.append([
                temps_total,
                [
                    self.position,
                    self.vitesse,
                    G
                ],
                indice
            ])

    def force(self, delta_h):
        if delta_h < 0:
            return (np.arctan(delta_h))*2/np.pi
        else:
            return (np.arctan(delta_h*0.1))*2/np.pi

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

    def definir_masse(self, masse):
        assert masse > 0
        self.masse = masse

    def definir_longueur(self, longueur):
        assert longueur > 0
        self.longueur = longueur

    def definir_force_acceleration(self, F_max):
        assert F_max > 0
        self.F_max = F_max

    def definir_force_freinage(self, F_min):
        assert F_min > 0
        self.F_min = F_min
