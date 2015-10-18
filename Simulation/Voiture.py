# coding: utf8

from math import exp

class Voiture(object):

    position = 0 # position en mètre
    vitesse = 0 # vitesse en m/s

    # Caractéristiques techniques
    masse = 1300 # masse en kg
    longueur = 4 # longueur en mètre
    F_max = 3000 # Force d'accélération maximum
    F_min = 3000 # Force de freinage maximum

    def __init__(self, position, vitesse):
        # Vitesse et position initiales de la voiture
        self.position = position
        self.vitesse = vitesse

    def update(self, delta, voiture_derriere, voiture_devant, vitesse_limite, distance_securite):
        # Influence de la voiture de devant
        if voiture_devant != None:
            distance = abs(self.position - voiture_devant.position) # Distance avec la voiture de devant
            delta_v = self.vitesse - voiture_devant.vitesse # Vitesse relative avec la voiture de devant
        else:
            distance = 1000000000
            delta_v = -1000000000

        # Calcul de la force appliquée par le conducteur
        F = self.F_max * (1 - exp(delta_v/vitesse_limite) * exp((distance_securite - distance) / distance_securite)) * (vitesse_limite - self.vitesse) / vitesse_limite

        F = min(F, self.F_max)
        F = max(F, -self.F_min)

        # Calcul de l'accélération via le PFD
        a = F / self.masse

        # Intégration d'Euler
        self.vitesse += a * delta
        self.position += self.vitesse * delta

        donnees = [
            self.position,
            self.vitesse,
            F
        ]

        return donnees