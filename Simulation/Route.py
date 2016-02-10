# coding: utf8

from Voiture import *
from Fonction import *
from pylab import *
from matplotlib import animation
from datetime import *
import pickle
import os



class Route(object):

    def __init__(self, longueur, vitesse_limite, delta, FCT):
        self.longueur = longueur # Longueur de la route en mètre
        self.vitesse_limite = vitesse_limite # Vitesse maximale autorisée en m/s sur toute section ! "vitesse limite suprême"

        self.voitures_valides = [] # Liste contenant les voitures valides
        self.voitures = [] # Liste contenant les voitures
        self.N_tot = 0 # Nombre de voitures sur la route
        self.N = 0 # Nombre de voitures sur la route valides
        self.FCT=FCT #[["f(x)",longueur]...]
                     #Attention : bien rentrer tableau de tableau
                     #Fonction de répartition initiale (Par morceaux ou non)        
        
        """ Tableau de données """
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []

        self.flux_active = True
        self.densite_active = True

        self.temps_total = 0 # Temps total de la simulation
        self.pas = 50 # Pas de mesure pour le flux et la densité
        self.delta = delta

        self.sections = [] # [position, longueur, vitesse_limite, temps_securite]

    def initialisation(self):   #À effectuer après ajout de toutes les sections
        self.voitures_valides = []
        self.voitures = []
        self.N_tot = 0
        self.N = 0

        """ Tableau de données """
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []

        self.flux_active = True
        self.densite_active = True

        self.temps_total = 0

        self.generer_trafic()

    def ajouter_section(self, longueur, vitesse_limite, temps_securite, indice=0):
        self.sections.insert(indice, [0, longueur, vitesse_limite, temps_securite])
        self.organise_sections()

    def affichage_section(self):
        """
        Affichage des sections sous forme de tableau avec alignement automatique
        """
        S = ["Numéro", "Position", "Longueur", "Vitesse maximale", "Temps de sécurité"]

        # Affichage de la liste des sommets avec alignement
        ligne = " "
        for s in S:
            ligne += s + " | "
        print(ligne)

        # Affichage de la matrice avec alignement
        n = 0
        for section in self.sections:
            l = (len(S[0]) + 2 - len(str(n)))/2
            if int(l) == l:
                l = int(l)
                ligne = " " * l +  str(n) + " " * l + "|"
            else:
                l = int(l)
                ligne = " " * l +  str(n) + " " * (l+1) + "|"
            n += 1
            i = 1
            for a in section:
                s = S[i]
                i += 1
                l = (len(s) + 2 - len(str(a)))/2
                if int(l) == l:
                    l = int(l)
                    ligne += " " * l +  str(a) + " " * l + "|"
                else:
                    l = int(l)
                    ligne += " " * l +  str(a) + " " * (l+1) + "|"

            print(ligne)

    def organise_sections(self):
        """
        Réorganise les sections en ajustant leur position de départ
        A effectuer après chaque supression ou ajout de section
        """
        if len(self.sections) > 1: # Il faut au moins 2 sections
            self.longueur = self.sections[0][1]
            for i in range(1, len(self.sections)):
                self.sections[i][0] = self.sections[i-1][0] + self.sections[i-1][1] # Ajuste le debut des sections selon: position en i = postion en i-1 + longueur de i-1
                self.longueur += self.sections[i][1] # Mise à jour de la longueur de la route

    def numero_section(self, position):
        """
        Renvoie l'indice de la section traversée par la voiture pour une position donnée à l'intérieur de la route
        """
        if position > self.longueur: # Si la voiture est en dehors de la route
            return 0 # renvoie la 1ère section
        for i in range(len(self.sections)):
            position -= self.sections[i][1]
            if position <= 0: # La voiture se situe alors dans la section numéro i
                return i
        return 0

    def desactiver_flux(self):
        if self.temps_total == 0:
            self.flux_active = False

    def desactiver_densite(self):
        if self.temps_total == 0:
            self.densite_active = False

    def generer_trafic(self):
        """FCT= voir Fonction(class)"""
        alpha=Fonction(self.FCT)
        P=alpha.position()
        
        
        while P:
            self.ajouter_voiture(P[0],self.sections[self.numero_section(P[0])][2])
            P.pop(0)

    def update(self, delta, temps_total, indice):

        self.temps_total = temps_total # Sauvegarde du temps total de simulation

        for voiture in self.voitures_valides:
            if voiture.valide:
                i = self.voitures_valides.index(voiture)
                if i != self.N-1:
                    voiture_devant = self.voitures_valides[i+1]
                else:
                    if self.N >= 2:
                        voiture_devant = self.voitures_valides[0]
                    else:
                        voiture_devant = None
                indice_section = self.numero_section(voiture.position)
                voiture.update(temps_total, delta, indice, voiture_devant, self.longueur, self.sections[indice_section][3], self.sections[indice_section][2])

        # On retire les voitures invalides de la simulation
        for voiture in self.voitures_valides:
            if not voiture.valide:
                self.retirer_voiture(voiture)

        # Mise à jour du flux de voitures
        if self.flux_active:
            F = []
            for k in range(0, self.longueur, self.pas):
                v_totale = 0
                for voiture in self.voitures_valides:
                    if voiture.position >= k and voiture.position < k + self.pas:
                        v_totale += voiture.vitesse
                F.append(v_totale / self.pas)

            self.flux.append([
                temps_total,
                F
            ])

        v = 0
        for voiture in self.voitures_valides:
            v += voiture.vitesse
        self.flux_total.append([
            temps_total,
            v / self.longueur
        ])

        if self.densite_active:
            # Mise à jour de la densité du trafic
            D = []
            for k in range(0, self.longueur, self.pas):
                v_totale = 0
                for voiture in self.voitures_valides:
                    if abs(voiture.position - k) < self.pas:
                        v_totale += 1
                D.append(v_totale / self.pas)

            self.densite.append([
                temps_total,
                D
            ])

        self.densite_totale.append([
            temps_total,
            self.N / self.longueur
        ])

    def ajouter_voiture(self, position, vitesse, index=0):
        voiture = Voiture(position, vitesse, self.vitesse_limite)
        self.voitures_valides.insert(index, voiture)
        self.voitures.append(voiture)
        self.N += 1
        self.N_tot += 1

    def retirer_voiture(self, voiture):
        self.voitures_valides.remove(voiture)
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
        ylim(0, self.longueur)
        xlim(0, self.temps_total)
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
        ylim(0, self.longueur)
        xlim(0, self.temps_total)
        show()

    def afficher_flux_densite(self):
        X = []
        Y = []

        for d in self.flux_total:
            Y.append(d[1])
        for d in self.densite_totale:
            X.append(d[1])

        # hist2d(np.array(X), np.array(Y), cmap="afmhot", bins=60)
        plot(X, Y, 'bo')
        xlim(0, max(X)*1.2)
        ylim(0, max(Y)*1.2)
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

    def analyse_voitures(self, nombre=-1):
        if nombre == -1:
            nombre = self.N_tot
        print("Analyse des positions...")
        for i in range(nombre):
            self.afficher_position(i)
        self.afficher(0, self.longueur, 0, self.temps_total)

        print("Analyse des vitesses...")
        for i in range(nombre):
            self.afficher_vitesse(i)
        self.afficher(0, self.temps_total, 0, 40)

        print("Analyse des forces...")
        for i in range(nombre):
            self.afficher_force(i)
        self.afficher(0, self.temps_total, -10000, 10000)

    def analyse_trafic(self):
        print("Analyse du flux...")
        if self.flux_active:
            self.afficher_flux()

        print("Analyse de la densité...")
        if self.densite_active:
            self.afficher_densite()

        print("Génération de la courbe flux-densité...")
        self.afficher_flux_densite()

    def animation(self):

        positions = []
        for voiture in self.voitures:
            positions.append(voiture.obtenir_positions(temps=False))

        fig = figure()
        data, = plot([], [], 'bo')
        xlim(0, self.longueur)
        ylim(0, 1)
        N = round(self.temps_total / self.delta)

        def update(k):
            X = []
            Y = []
            for voiture in positions:
                try:
                    i = voiture[0].index(k)
                    position = voiture[1][i]
                    X.append(position)
                    Y.append(0.5)
                except:
                    pass
            data.set_data(X, Y)
            title("Temps : " + str(round(self.delta * k)) + "s")
            return data

        animation.FuncAnimation(fig, update, frames=N, interval=self.delta/1000, repeat=False)
        legend()
        show()

    def sauvegarde(self):
        """
        Fonction qui sauvegarde dans un fichier les données de la simulation
        """
        d = datetime.now()
        nom_fichier = str(d.day) + "-" + str(d.month) + "-" + str(d.year) + "_" + str(d.hour) + str(d.minute) + str(d.second) + str(d.microsecond)
        print("Sauvegarde dans le fichier : Données/" + nom_fichier)

        with open(os.getcwd() + "/Données/" + nom_fichier, 'wb') as fichier:
            p = pickle.Pickler(fichier)
            """ Enregistrement des données de la simualation """
            # Paramètres de la simulation
            p.dump([
                self.temps_total,
                self.delta,
                self.longueur
            ])

            p.dump(self.flux_total)
            p.dump(self.densite_totale)
