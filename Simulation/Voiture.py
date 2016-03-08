# coding: utf8

from Modele import *


class Voiture(object):

    def __init__(self, position, vitesse, delta, temps_total, indice, numero_section):
        """
        Initialisation de la classe Voituresimulation
        :param position: position initiale en mètres
        :param vitesse: vitesse initiale en mètres par seconde
        :param delta: pas de temps de la simulation
        :param temps_total: temps total de la simulation
        :param indice: nombre de tours dans la boucle effectués
        """

        self.donnees = []  # Tableau contenant les données enregistrées lors de la simulation
        self.position = position
        self.position_totale = position  # Position sur la route sans le retour à l'origine lors d'une boucle
        self.vitesse = vitesse
        self.longueur = 4  # Longueur en mètre de la voiture
        self.a_max = 20  # Accélération maximale en m/s²
        self.a_min = 20  # Décélération maximale en m/s²
        self.valide = True  # Booléen pour savoir si la voiture doit être prise en compte dans la simulation
        self.temps_reaction = 2  # Temps de réaction commun aux conducteurs en secondes
        # Création du modèle pour la gestion de l'accélération
        self.modele = Modele(self.a_max, self.a_min, self.temps_reaction, self.longueur)
        self.numero_section = numero_section  # Numéro de la section dans laquelle se situe la voiture
        self.premiere = False  # Indique si la voiture est la première sur la route

        # Création de données pour les positions et les vitesses pour le temps de réaction
        indice_decalage = int(self.temps_reaction / delta) + 1
        for i in range(indice_decalage):
            self.donnees.append([
                temps_total + delta * i - delta * indice_decalage,
                [
                    self.position,
                    self.position_totale,
                    self.vitesse,
                    0
                ],
                indice + i - indice_decalage
            ])

    def update(self, temps_total, delta, indice, voiture_devant, longueur, vitesse_limite, boucle=True):
        """
        Mise à jour de la voiture
        :param temps_total: temps total de la simulation
        :param delta: pas de temps d'intégration
        :param indice: nombre de tours dans la boucle effectués
        :param voiture_devant: objet Voiture, voiture qui la précède
        :param longueur: longueur de la route
        :param vitesse_limite: vitesse maximale autorisée sur la section
        :param boucle: booleén qui indique si la route boucle sur elle même
        """

        if self.position >= longueur:
            if boucle:
                self.position -= longueur
            else:
                self.valide = False
                return None

        # Influence de la voiture de devant
        if voiture_devant is not None:
            """ Intégration du temps de réaction """
            # L'indice de décalage représente le décalage dans la prise d'information du conducteur
            # Ainsi, on récupère les données de la voiture de devant en prenant en compte ce décalage
            indice_decalage = indice - round(self.temps_reaction / delta) - 1

            # Récupération des données de la voiture de devant
            v, d = voiture_devant.obtenir_vitesse_position(indice_decalage)

            # Distance relative
            distance = d - self.position_totale
            if distance <= 0:
                if self.premiere:  # Cas particulier de la première voiture
                    if boucle:
                        distance += longueur
                    else:
                        distance += 1000000
                else:  # Sinon c'est un dépassement non voulu
                    distance = -1000000
        else:
            distance = 1000000
            v = 100000

        # Calcul de l'accélération appliquée par le conducteur
        a = self.modele.calcul_acceleration(v, self.vitesse, distance, vitesse_limite)

        # On limite l'accélération
        a = min(a, self.a_max)
        a = max(a, -self.a_min)

        # Intégration d'Euler
        self.vitesse += a * delta
        if self.vitesse < 0:  # Impossible de reculer
            self.vitesse = 0
        self.position += self.vitesse * delta
        self.position_totale += self.vitesse * delta

        # Enregistrement des données
        self.donnees.append([
            temps_total,
            [
                self.position,
                self.position_totale,
                self.vitesse,
                a
            ],
            indice
        ])

    def obtenir_positions(self, temps=True):
        """
        :param temps: booléen qui permet de choisir entre temps ou indice
        :return: une liste contenant les positions de la voiture en fonction du temps ou de l'indice
        """
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

    def obtenir_vitesse_position(self, i):
        """
        :param i: indice
        :return: la vitesse et la position de la voiture à l'indice i
        """

        j = len(self.donnees) - 1
        while j >= 0:
            d = self.donnees[j]
            if d[2] == i:
                return d[1][2], d[1][1]
            j -= 1

    def obtenir_vitesse(self, i):
        """
        :param i: indice
        :return: la vitesse de la voiture à l'indice i
        """
        j = len(self.donnees) - 1
        while j >= 0:
            d = self.donnees[j]
            if d[2] == i:
                return d[1][2]
            j -= 1

    def obtenir_position(self, i):
        """
        :param i: indice
        :return: la position de la voiture à l'indice i
        """
        j = len(self.donnees) - 1
        while j >= 0:
            d = self.donnees[j]
            if d[2] == i:
                return d[1][0]
            j -= 1

    def obtenir_position_totale(self, i):
        """
        :param i: indice
        :return: la position de la voiture à l'indice i
        """
        j = len(self.donnees) - 1
        while j >= 0:
            d = self.donnees[j]
            if d[2] == i:
                return d[1][1]
            j -= 1

    def obtenir_vitesses(self):
        """
        :return: une liste contenant les vitesses de la voiture en fonction du temps
        """
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][2])
        return t, r

    def obtenir_acceleration(self):
        """
        :return: une liste contenant les accélérations de la voiture en fonction du temps
        """
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][3])
        return t, r
