# coding: utf8

from Voiture import *
from pylab import *


class Route(object):
    """
    Classe repésentant une route à plusieurs voies de circulation.
    """

    def __init__(self, longueur = 1000, vitesse_limite = 36):
        self.longueur = longueur # Longueur de la route en mètre
        self.vitesse_limite = vitesse_limite # Vitesse maximale autorisée en m/s
        self.distance_securite = 2 * self.vitesse_limite # Distance mimimale entre deux voitures

        self.voitures = [] # Liste contenant les voitures
        self.N = 0 # Nombre de voitures sur la route

        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []
        self.temps_total = 0 # Temps total de la simulation
        self.pas = 50 # Pas de mesure pour le flux et la densité
        self.timer = 0
        self.frequence = 1/4

    def initialisation(self):
        self.distance_securite = 2 * self.vitesse_limite
        self.voitures = [] # Liste contenant les voitures
        self.N = 0 # Nombre de voitures sur la route
        self.flux = []
        self.densite = []
        self.temps_total = 0

    def update(self, delta, temps_total):
        self.timer += delta
        if self.timer >= 1/self.frequence:
            self.timer -= 1/self.frequence
            self.ajouter_voiture(0, 36)

        self.temps_total = temps_total
        for voiture in self.voitures:
            if voiture.valide:
                i = self.voitures.index(voiture)
                if i != 0:
                    voiture_derriere = self.voitures[i-1]
                else:
                    voiture_derriere = None
                if i != self.N-1:
                    voiture_devant = self.voitures[i+1]
                    if not voiture_devant.valide:
                        voiture_devant = None
                else:
                    voiture_devant = None
                voiture.update(temps_total, delta, voiture_derriere, voiture_devant, self.vitesse_limite, self.distance_securite, self.longueur)

        # Mise à jour du flux de voitures
        F = []
        for k in range(0, self.longueur, self.pas):
            v_totale = 0
            for voiture in self.voitures:
                if voiture.position >= k and voiture.position < k + self.pas and voiture.valide:
                    v_totale += voiture.vitesse
            F.append(v_totale / self.pas)

        self.flux.append([
            temps_total,
            F
        ])

        v = 0
        for voiture in self.voitures:
            if voiture.valide:
                v += voiture.vitesse
        self.flux_total.append([
            temps_total,
            v / self.longueur
        ])

        # Mise à jour de la densité du trafic
        D = []
        for k in range(0, self.longueur, self.pas):
            v_totale = 0
            for voiture in self.voitures:
                if abs(voiture.position - k) < self.pas and voiture.valide:
                    v_totale += 1
            D.append(v_totale / self.pas)

        self.densite.append([
            temps_total,
            D
        ])

        N = 0
        for voiture in self.voitures:
            if voiture.valide:
                N += 1
        self.densite_totale.append([
            temps_total,
            N / self.longueur
        ])

    def ajouter_voiture(self, position, vitesse):
        voiture = Voiture(position, vitesse)
        self.voitures.insert(0, voiture)
        self.N += 1

    def retirer_voiture(self, voiture):
        self.voitures.remove(voiture)
        self.N -= 1

    def liste_vide(self, taille):
        R = []
        for i in range(0, taille):
            R.append([])
        return R

    def afficher_flux(self):
        Z = []
        X = []
        Y = [k for k in range(0, self.longueur + self.pas, self.pas)]
        for d in self.flux:
            X.append(d[0])
            Z.append(d[1])

        m = np.matrix(Z)

        pcolor(np.array(X), np.array(Y), np.array(m.T), cmap="afmhot")
        show()

    def afficher_densite(self):
        Z = []
        X = []
        Y = [k for k in range(0, self.longueur + self.pas, self.pas)]
        for d in self.densite:
            X.append(d[0])
            Z.append(d[1])

        m = np.matrix(Z)

        pcolor(np.array(X), np.array(Y), np.array(m.T), cmap="afmhot")
        show()

    def afficher_flux_densite(self):
        X = []
        Y = []
        for d in self.flux_total:
            Y.append(d[1])
        for d in self.densite_totale:
            X.append(d[1])
        hist2d(np.array(X), np.array(Y), cmap="afmhot", bins=60)
        show()

    def afficher_position(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_positions()
        plot(Y, X)

    def afficher_vitesse(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_vitesses()
        plot(X, Y)

    def afficher_force(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_forces()
        plot(X, Y)

    def afficher_distance(self, i1, i2):
        try:
            voiture1 = self.voitures[i1]
            voiture2 = self.voitures[i2]
        except:
            print("Erreur ! Impossible de récupérer les voitures d'indices " + str(i1) + " et " + str(i2))
            return None
        X, Y1 = voiture1.obtenir_positions()
        X, Y2 = voiture2.obtenir_positions()
        Y = []
        D = []
        for i in range(len(Y1)):
            Y.append(Y2[i] - Y1[i])
            D.append(self.distance_securite)
        plot(X, Y, label="Distance entre les voitures " + str(i1) + " et " + str(i2))

    def afficher(self, xmin, xmax, ymin, ymax):
        xlim(xmin, xmax)
        ylim(ymin, ymax)
        legend(loc="best")
        show()

    def analyse_voitures(self):
        print("Analyse des positions...")
        for i in range(self.N):
            self.afficher_position(i)
        self.afficher(0, self.longueur, 0, self.temps_total)

        print("Analyse des vitesses...")
        for i in range(self.N):
            self.afficher_vitesse(i)
        self.afficher(0, self.temps_total, 0, 40)

        print("Analyse des forces...")
        for i in range(self.N):
            self.afficher_force(i)
        self.afficher(0, self.temps_total, -6100, 6100)

    def analyse_trafic(self):
        print("Analyse du flux...")
        self.afficher_flux()

        print("Analyse de la densité...")
        self.afficher_densite()

        print("Génération de la courbe flux-densité...")
        self.afficher_flux_densite()