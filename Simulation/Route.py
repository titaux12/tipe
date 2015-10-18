# coding: utf8

from Voiture import *
from pylab import *

class Route(object):
    """
    Classe repésentant une route à plusieurs voies de circulation.
    """

    longueur = 0 # Longueur de la route en mètre
    vitesse_limite = 0 # Vitesse maximale autorisée en m/s
    distance_securite = 0 # Distance mimimale entre deux voitures

    voitures = [] # Liste contenant les voitures
    N = 0 # Nombre de voitures sur la route

    donnees = []
    flux = []
    densite = []

    def __init__(self, longueur = 1000, vitesse_limite = 36):
        self.longueur = longueur
        self.vitesse_limite = vitesse_limite

    def initialisation(self):
        self.distance_securite = 2 * self.vitesse_limite
        d = 0
        while d < self.longueur:
            self.ajouter_voiture(d, 0)
            d += self.distance_securite

    def update(self, delta, temps_total):
        donnees_temp = []
        for voiture in self.voitures:
            if voiture.position >= self.longueur:
                self.retirer_voiture(voiture)
                self.ajouter_voiture(0, 0)
            else:
                i = self.voitures.index(voiture)
                if i != 0:
                    voiture_derriere = self.voitures[i-1]
                else:
                    voiture_derriere = None
                if i != self.N-1:
                    voiture_devant = self.voitures[i+1]
                else:
                    voiture_devant = None

                donnee = voiture.update(
                    delta,
                    voiture_derriere,
                    voiture_devant,
                    self.vitesse_limite,
                    self.distance_securite,
                )
                donnees_temp.append(donnee)
        self.donnees.append([temps_total, donnees_temp])
        self.densite.append(self.N / self.longueur)
        v = 0
        for voiture in donnees_temp:
            v += voiture[1]
        self.flux.append(v / self.longueur)

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

    def afficher_graphique(self):
        T = []
        V = self.liste_vide(self.N)
        P = self.liste_vide(self.N)
        F = self.liste_vide(self.N)
        for d in self.donnees:
            T.append(d[0])
            for i in range(0, self.N):
                try:
                    V[i].append(d[1][i][1])
                except:
                    V[i].append(0)
            for i in range(0, self.N):
                try:
                    P[i].append(d[1][i][0])
                except:
                    P[i].append(0)
            for i in range(0, self.N):
                try:
                    F[i].append(d[1][i][2])
                except:
                    F[i].append(0)

        #for v in V:
        #    plot(T, v, label="voiture " + str(V.index(v)))
        #for p in P:
        #    plot(T, p, label="voiture " + str(P.index(p)))
        #for f in F:
        #    plot(T, f, label="voiture " + str(F.index(f)))
        #plot(T, self.densite)
        #plot(self.flux, self.densite)
        legend(loc="best")
        show()