# coding: utf8

from Voiture import *
from pylab import *


class Route(object):
    """
    Classe repésentant une route à plusieurs voies de circulation.
    """

    def __init__(self, longueur = 30000, vitesse_limite = 36):
        self.longueur = longueur # Longueur de la route en mètre
        self.vitesse_limite = vitesse_limite # Vitesse maximale autorisée en m/s
        self.distance_securite = 2 * self.vitesse_limite # Distance mimimale entre deux voitures

        self.voitures = [] # Liste contenant les voitures
        self.N = 0 # Nombre de voitures sur la route

        self.flux = []
        self.densite = []

    def initialisation(self):
        self.distance_securite = 2 * self.vitesse_limite
        self.voitures = [] # Liste contenant les voitures
        self.N = 0 # Nombre de voitures sur la route
        self.flux = []
        self.densite = []

        self.ajouter_voiture(0, 0)
        self.ajouter_voiture(10, 0)

    def update(self, delta, temps_total):
        for voiture in self.voitures:
            i = self.voitures.index(voiture)
            if i != 0:
                voiture_derriere = self.voitures[i-1]
            else:
                voiture_derriere = None
            if i != self.N-1:
                voiture_devant = self.voitures[i+1]
            else:
                voiture_devant = None
            voiture.update(temps_total, delta, voiture_derriere, voiture_devant, self.vitesse_limite, self.distance_securite)

    def ajouter_voiture(self, position, vitesse):
        voiture = Voiture(position, vitesse)
        self.voitures.append(voiture)
        self.N += 1

    def retirer_voiture(self, voiture):
        self.voitures.remove(voiture)
        self.N -= 1

    def liste_vide(self, taille):
        R = []
        for i in range(0, taille):
            R.append([])
        return R

    def afficher_position(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_positions()
        plot(X, Y, label="Voiture " + str(indice))

    def afficher_vitesse(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_vitesses()
        plot(X, Y, label="Voiture " + str(indice))

    def afficher_force(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_forces()
        plot(X, Y, label="Voiture " + str(indice))

    def afficher(self, xmin, xmax, ymin, ymax):
        xlim(xmin, xmax)
        ylim(ymin, ymax)
        legend(loc="best")
        show()