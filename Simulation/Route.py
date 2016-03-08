# coding: utf8

from Voiture import *
from pylab import *
from matplotlib import animation
from datetime import *
import pickle
import os


class Route(object):

    def __init__(self, delta):
        """
        Initialisation de la classe Voiture
        :param delta: pas de temps d'intégration de la simulation
        """
        self.longueur = 0  # Longueur de la route en mètres
        self.delta = delta
        self.temps_total = 0
        self.indice = 0
        self.boucle = True

        self.voitures_valides = [] # Liste contenant les voitures valides uniquement
        self.voitures = []  # Liste contenant toutes les voitures
        self.N_tot = 0  # Nombre de voitures total sur la route
        self.N = 0  # Nombre de voitures valides sur la route

        """ Tableau de données """
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []

        # Permet de ne pas enregistrer (et donc calculer) les flux et/ou densités sur la route
        self.flux_active = True
        self.densite_active = True

        self.pas = 50  # Pas de distance pour le calcul du flux et de la densité

        """
        Liste contenant les données relatives aux sections de la route,
        selon le format suivant: [position_debut, longueur, vitesse_limite]
        """
        self.sections = []

    def preparation(self, fonction, pas=1, verification=True):
        """
        Permet d'initialiser toutes les valeurs de la classe Route à leur valeur par defaut,
        et lance la génération du trafic routier initial (t=0)
        :param fonction: fonction python qui donne la densité du trafic en fonction de la position x
        :param pas: le pas pour le calcul de l'aire
        :param verification: booléen qui permet de ne pas vérifier la génération du trafic routier
        """
        self.voitures_valides = []
        self.voitures = []
        self.N_tot = 0
        self.N = 0
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []
        self.flux_active = True
        self.densite_active = True
        self.temps_total = 0
        self.indice = 0

        self.organisation_sections()

        self.generer_trafic(fonction)

    def ajouter_section(self, longueur, vitesse_limite, indice=0):
        """
        Ajoute une section à la liste des sections dèjà existantes
        :param longueur: longueur en mètre
        :param vitesse_limite: vitesse maximale autorisée sur la route en mètres par seconde
        :param indice: emplacement de la section dans la route, par défaut au début de la route
        """
        self.sections.insert(indice, [0, longueur, vitesse_limite])

    def affichage_section(self):
        """
        Affichage des sections sous forme de tableau avec alignement automatique
        """
        S = ["Numéro", "Position", "Longueur", "Vitesse maximale"]

        # Affichage de la liste S avec alignement
        ligne = " "
        for s in S:
            ligne += s + " | "
        print(ligne)

        # Affichage des sections avec alignement
        n = 0
        for section in self.sections:
            l = (len(S[0]) + 2 - len(str(n)))/2
            if int(l) == l:
                l = int(l)
                ligne = " " * l + str(n) + " " * l + "|"
            else:
                l = int(l)
                ligne = " " * l + str(n) + " " * (l+1) + "|"
            n += 1
            i = 1
            for a in section:
                s = S[i]
                i += 1
                l = (len(s) + 2 - len(str(a)))/2
                if int(l) == l:
                    l = int(l)
                    ligne += " " * l + str(a) + " " * l + "|"
                else:
                    l = int(l)
                    ligne += " " * l + str(a) + " " * (l+1) + "|"

            print(ligne)

    def organisation_sections(self):
        """
        Réorganisation des sections en ajustant leur position de départ
        """
        self.longueur = self.sections[0][1]  # Longueur de la route
        if len(self.sections) > 1:  # Il faut au moins 2 sections
            for i in range(1, len(self.sections)):
                # Ajuste le début des sections selon: position en i = position en i-1 + longueur de i-1
                self.sections[i][0] = self.sections[i-1][0] + self.sections[i-1][1]
                self.longueur += self.sections[i][1]  # Mise à jour de la longueur de la route

    def numero_section(self, position, numero_precedent=-1):
        """
        Renvoie l'indice de la section traversée par la voiture pour une position donnée à l'intérieur de la route
        :param position: la position de la voiture
        :param numero_precedent: le numéro de la section ou se trouve la voiture
        :return: le numéro de la section à la position entrée en paramètre
        """
        if numero_precedent >= 0:
            section = self.sections[numero_precedent]
            if position >= section[0] + section[1]:
                if position <= self.longueur:
                    return numero_precedent + 1
                else:
                    return 0
                pass
            else:
                return numero_precedent
        else:
            if position <= self.longueur:  # On vérifie que la voiture est dans la route
                for i in range(0, len(self.sections)):
                    position -= self.sections[i][1]
                    if position <= 0:  # La voiture se situe alors dans la section
                        return i
            else:
                return 0

    def desactiver_flux(self):
        if self.temps_total == 0:  # Uniquement au début de la simulation
            self.flux_active = False

    def desactiver_densite(self):
        if self.temps_total == 0:  # Uniquement au début de la simulation
            self.densite_active = False

    def generer_trafic(self, fonction, affichage=False):
        """
        Génération du trafic routier initial
        :param fonction: fonction python qui donne la densité du trafic en fonction de la position x
        :param verification: booléen qui permet de ne pas vérifier la génération du trafic routier
        """
        pas=1
        taille_voiture=4        
        x_prec=0 #x precedent
        positions = []  # Liste contenant la position des voitures
        Y = []  # Utile uniquement pour l'affichage
        aire = 0
        for x in range(0, self.longueur, pas):
            D = fonction(x)
            aire += D * pas
            if int(aire) >= 1:  # Si on a au moins une voiture
                if x - x_prec < taille_voiture: #Si les voitures ne sont pas distante de taille_voiture
                    return False
                x_prec = x
                positions.append(x)
                Y.append(int(aire))
                aire -= int(aire)
                
                        
        if affichage:
            plot(positions, Y, 'bo')
            ylim(0, 2)
            xlim(0, self.longueur)
            show()

            confirmation = input("Conservez vous la répartition initial ? o/n")
            if confirmation != "o":
                return False
            

        l = len(positions)
        for x in range(0, l):
            position = positions[l - x - 1]
            section = self.numero_section(position)
            self.ajouter_voiture(position, self.sections[section][2], section)

        self.voitures_valides[l-1].premiere = True  # On marque la première voiture
        print("Génération du trafic réussie")
        
        return True

    def update(self, delta, temps_total, indice):
        """
        Mise à jour de la route et de chaque voiture
        :param delta: pas de temps d'intégration de la simulation
        :param temps_total: temps total de la simulation
        :param indice: nombre de tours dans la boucle effectués
        """

        self.temps_total = temps_total  # Sauvegarde du temps total de simulation
        self.indice = indice

        vitesse_totale = 0

        for j in range(self.N):
            i = self.N - j - 1
            voiture = self.voitures_valides[i]
            if i != self.N-1:  # Si la voiture n'est pas la première
                voiture_devant = self.voitures_valides[i+1]
            else:  # Si c'est la première voiture
                if self.N >= 2 and self.boucle:  # S'il y a plus de 2 voitures alors la voiture de devant est la première
                    voiture_devant = self.voitures_valides[0]
                else:
                    voiture_devant = None
            indice_section = self.numero_section(voiture.position, numero_precedent=voiture.numero_section)
            # Mise à jour de la voiture
            voiture.update(
                temps_total,
                delta,
                indice,
                voiture_devant,
                self.longueur,
                self.sections[indice_section][2],  # vitesse limite
                boucle=self.boucle
            )

            vitesse_totale += voiture.vitesse

        # On retire les voitures invalides de la simulation
        for voiture in self.voitures_valides:
            if not voiture.valide:
                self.retirer_voiture(voiture)

        # Mise à jour du flux
        if self.flux_active:
            F = []
            for k in range(0, self.longueur, self.pas):  # On découpe la route en intervalle de longueur 'self.pas'
                v_totale = 0
                for voiture in self.voitures_valides:
                    if voiture.position <= k + self.pas and voiture.position >= k:
                        v_totale += voiture.vitesse
                F.append(v_totale / self.pas)

            self.flux.append([
                temps_total,
                F
            ])

        self.flux_total.append([
            temps_total,
            vitesse_totale / self.longueur
        ])

        # Mise à jour de la densité
        if self.densite_active:
            D = []
            for k in range(0, self.longueur, self.pas):
                N_totale = 0
                for voiture in self.voitures_valides:
                    if voiture.position <= k + self.pas and voiture.position >= k:
                        N_totale += 1
                D.append(N_totale / self.pas)

            self.densite.append([
                temps_total,
                D
            ])

        self.densite_totale.append([
            temps_total,
            self.N / self.longueur
        ])

    def ajouter_voiture(self, position, vitesse, numero_section, index=0):
        """
        Ajoute une voiture dans la simulation
        :param position: position initiale en mètres
        :param vitesse: vitesse initiale en mètres par seconde
        :param numero_section: numéro de la section de départ
        :param index: emplacement de la voiture sur la route, par défaut derrière toutes les autres
        """
        voiture = Voiture(position, vitesse, self.delta, self.temps_total, self.indice, numero_section)
        self.voitures_valides.insert(index, voiture)
        self.voitures.append(voiture)
        self.N += 1
        self.N_tot += 1

    def retirer_voiture(self, voiture):
        """
        Retire une voiture de la simulation
        :param voiture: objet Voiture à retirer
        """
        self.voitures_valides.remove(voiture)
        self.N -= 1

    """
    Début des fonctions pour l'affichage de graphiques,
    liste des graphiques disponibles:
        - flux en fonction de la position et du temps
        - densité en fonction de la position et du temps
        - flux en fonction de la densité (permet de générer la courbe caractéristique des différents régimes de trafic)
        - positions, vitesses, accélérations en fonction du temps pour un certain nombre de voitures
        - distance entre deux voitures en fonction du temps (permet de vérifier le respect des distances de sécurité)
        - animation qui permet d'observer la simulation une fois finie
    """

    def afficher_flux(self):
        Z = []
        maxi = []
        for d in self.flux:
            maxi.append(max(d[1]))
            Z.append(d[1])

        m = matrix(Z)

        imshow(m.T, interpolation="none", cmap="afmhot", aspect="auto", vmin=0, vmax=max(maxi), origin="lower", extent=[0, self.temps_total, 0, self.longueur])
        colorbar()

        show()

    def afficher_densite(self):
        Z = []
        maxi = []
        for d in self.densite:
            maxi.append(max(d[1]))
            Z.append(d[1])

        m = matrix(Z)

        imshow(m.T, interpolation="none", cmap="afmhot", aspect="auto", vmin=0, vmax=max(maxi), origin="lower", extent=[0, self.temps_total, 0, self.longueur])
        colorbar()

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

    def afficher_acceleration(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_acceleration()
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
        nombre = int(self.N_tot / 10) + 1

        print("Analyse des positions...")
        for i in range(nombre):
            self.afficher_position(i)
        self.afficher(0, self.longueur, 0, self.temps_total)

        print("Analyse des vitesses...")
        for i in range(nombre):
            self.afficher_vitesse(i)
        self.afficher(0, self.temps_total, 0, 40)

        print("Analyse des accélérations...")
        for i in range(nombre):
            self.afficher_acceleration(i)
        self.afficher(0, self.temps_total, -30, 30)

    def analyse_trafic(self):
        if self.flux_active:
            print("Analyse du flux...")
            self.afficher_flux()

        if self.densite_active:
            print("Analyse de la densité...")
            self.afficher_densite()

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
        Permet de sauvegarder dans un fichier les données de la simulation dans le dossier 'Données',
        dans le but de les afficher simultanément via le fichier 'Analyse.py'
        """
        d = datetime.now()
        nom_fichier = str(d.day) + "-" + str(d.month) + "-" + str(d.year) + "_" + str(d.hour) + str(d.minute) + str(d.second) + str(d.microsecond)
        print("Sauvegarde dans le fichier : Données/" + nom_fichier)

        with open(os.getcwd() + "/Simulation/Données/" + nom_fichier, 'xb') as fichier:
            p = pickle.Pickler(fichier)
            """ Enregistrement des données de la simualation """
            # Paramètres de la simulation
            p.dump([
                self.temps_total,
                self.delta,
                self.longueur
            ])

            # Calcul de la vitesse moyenne sur la route
            if self.N != 0:
                vitesse_moyenne = 0
                for voiture in self.voitures_valides:
                    vitesse_moyenne += voiture.vitesse
                vitesse_moyenne /= self.N

            p.dump(self.flux_total)
            p.dump(self.densite_totale)
            p.dump(vitesse_moyenne)
