from pylab import *
from random import *
import matplotlib.animation as anim

class Reseau():
    """
    Classe Reseau
    """

    """
    Caractéristiques liées au graphe
    """
    A = [] # Matrice de valuation
    S = [] # Sommets du graphe

    """
    Caractéristiques liées au réseau
    """
    F = [] # Matrice des flots
    C = [] # Matrice des capacités

    """
    Mesures globales du réseau
    """
    """   Taille du réseau    """
    n = 0 # Nombre de liens
    e = 0 # Nombre de sommets
    p = 0 # Composants
    D = 0 # Diamètre
    L = 0 # Longueur totale : Somme des longueurs des liens
    Q = 0 # Trafic total : Somme des trafics des liens
    s = 0 # Surface de l'espace étudié

    """    Organisation du réseau   """
    DI = 0 # Indice de détour : Longueur du graphe rapportée à la longueur du réseau
    ND = 0 # Densité : Longueur du graphe rapportée à la surface de l'espace étudié
    Pi = 0 # Indice Pi a : Longueur du graphe rapportée au nombres de liens
    Theta = 0 # Indice Theta : Trafic total rapporté au nombre de sommets

    """    Structure   """
    u = 0 # Nombre cyclomatique : Nombre maximum de cycles indépendants
    Alpha = 0 # Indice Alpha : Nombre de cycles sur nombre maximum de cycles possibles
    Beta = 0 # Indice Beta : Nombre de liens sur nombre de sommets
    Gamma = 0 # Indice Gamma : Nombre de liens sur nombre maximum de liens possibles
    C = 0 # Cent: Longueur du graphe rapportée à la longueur du diamètre
    Eta = 0 # Indice Etralité : Somme des centralités individuelles des noeuds

    def __init__(self, s=[], a=[], c=[]):
        """
        :param s: Liste des sommets du graphe
        :param a: Matrice de valuation du graphe
        :param c: Matrice des capacités
        """

        if len(s) == 0:
            print("Il doit y avoir un minimum de 1 noeud dans le réseau !")
            print("Création d'un noeud de base")
            s = ['A']

        if not self.validation_matrice(s, a):
            print("La matrice de valuation est invalide !")
            print("Création d'une matrice vide")
            a = self.matrice_vide(len(s))

        if not self.validation_matrice(s, c):
            print("La matrice des capacités est invalide !")
            print("Création d'une matrice vide")
            c = self.matrice_vide(len(s))

        self.S = s
        self.A = a
        self.C = c

        # Initialisation de la matrice des flots
        self.F = self.matrice_vide(len(self.S))

    def v(self, s1, s2):
        """
        Valuation du graphe
        :param s1: sommet de départ
        :param s2: sommet d'arrivée
        :return: la valuation de l'arc correspondant
        """
        x = self.S.index(s1)
        y = self.S.index(s2)
        return self.A[x][y]

    def ajouter_noeud(self, s):
        """
        Ajoute un noeud au réseau
        :param s: nom du noeud
        """
        self.S.append(s)
        l = len(self.S)

        for i in range(0, l - 1):
            self.A[i].append(inf)
            self.F[i].append(0)
            self.C[i].append(0)

        self.A.append([])
        self.F.append([])
        self.C.append([])

        for i in range(0, l):
            self.A[l - 1].append(inf)
            self.F[l - 1].append(0)
            self.C[l - 1].append(0)

    def ajouter_lien(self, s1, s2, v):
        """
        Ajoute un lien entre deux noeuds dans le réseau
        :param s1: sommet de départ
        :param s2: sommet d'arrivée
        :param v: valeur du lien
        """
        x = self.S.index(s1)
        y = self.S.index(s2)
        self.A[x][y] = v

    def matrice_vide(self, l):
        """
        Initialisation d'une matrice carrée vide de taille l
        :param l: la taille de la matrice
        :return:
        """
        R = []
        for i in range(0, l):
            a = []
            for j in range(0, l):
                a.append(0)
            R.append(a)
        return R

    def mise_a_jour_flot(self, s1, s2, v):
        """
        Met à jour les flots
        :param s1: sommet de départ
        :param s2: sommet d'arrivée
        :param v: nouvelle valeur du flot entre s1 et s2
        """
        x = self.S.index(s1)
        y = self.S.index(s2)
        c = self.C[x][y]
        if v <= c: # On regarde si la capacité n'est pas atteinte
            self.F[x][y] = v
        # else:
        #     print("La capacité (" + str(c) + ") entre " + s1 + " et " + s2 + " a été dépassée (" + str(v) + ") !")

    def validation_matrice(self, s, m):
        """
        Validation des données du graphe :
        La matrice doit être carrée de taille le nombre de sommets
        :param s: liste des sommets
        :param m: matrice à tester
        :return: vrai si la matrice est valide, faux sinon
        """
        if len(m) != len(s):
            return False
        for ligne in m:
            if len(ligne) != len(s):
                return False
        return True

    def afficher_flot_capacite(self):
        """
        Affiche la matrice des flots et des capacités
        :return:
        """
        l = len(self.S)
        R = self.matrice_vide(l)
        for i in range(0, l):
            for j in range(0, l):
                R[i][j] = str(self.F[i][j]) + "/" + str(self.C[i][j])
        self.afficher_matrice(R)

    def afficher_matrice(self, matrice):
        """
        Affiche une matrice liée au graphe
        :param matrice: matrice à afficher
        """

        if len(self.S) == 0:
            print("Aucune donnée dans le graphe à afficher")
            return 0

        n = len(self.S)

        # Recherche de la longueur du plus grand élément de la matrice de valuation
        m1 = max(max(len(str(l)) for l in ligne) for ligne in matrice) + 1

        # Recherche de la longueur du nom de sommet le plus grand
        m2 = max(len(str(s)) for s in self.S) + 1

        # Maximum global
        m = max(m1, m2)

        # Affichage de la liste des sommets avec alignement
        ligne = " " * m2 + "|"
        for i in range(0, n):
            s = self.S[i]
            ligne += " " * (m - len(str(s))) + str(s)
        print(ligne)

        # Affichage de la matrice avec alignement
        for i in range(0, n):
            ligne = ""
            s = self.S[i]
            ligne += str(s) + " " * (m2 - len(str(s))) + "|"
            for j in range(0, n):
                a = matrice[i][j]
                ligne += " " * (m - len(str(a))) + str(a)
            print(ligne)

    def simulation(self, n):
        """
        Lance une simulation sur n points
        :param n: nombre max d'itérations
        """

        def update(i):
            """
            Fonction de mise à jour du réseau
            :param i: numéro de la frame courante
            """
            ax.clear()
            X, Y = self.position_noeuds()
            self.plot(ax, rayon, couleur, X, Y, capacite=True)
            axis('scaled')
            print("frames : " + str(i))

        fig = figure(figsize=(12, 12), dpi=80)

        ax = fig.add_subplot(111)

        # Positions des noeuds dans le graphe
        X, Y = self.position_noeuds()

        rayon = self.calcul_taille_noeuds(rmin=0.2, rmax=0.5)

        couleur = self.calcul_couleur_noeuds()

        self.plot(ax, rayon, couleur, X, Y, capacite=True)

        axis('scaled')
        anim.FuncAnimation(fig, update, frames=n, interval=1000, repeat=False)
        show()

    def plot(self, ax, rayon, couleur, X, Y, capacite=False):
        """
        Création des cercles, des flèches et des textes
        :param ax:
        :param rayon:
        :param couleur:
        :param X:
        :param Y:
        :param capacite:
        :return:
        """
        l = len(self.S)
        # Création des cercles
        for i in range(0, l):
            c = Circle((X[i], Y[i]), radius=rayon[i], color=couleur[i], alpha=1)
            ax.add_patch(c)

        # Créations des liens
        for i in range(0, l):
            for j in range(0, l):
                if self.A[i][j] != inf: # si un lien existe entre les deux noeuds
                    if i != j:
                        # coordonnées de départ
                        x = X[i]
                        y = Y[i]

                        # Direction de la flèche
                        dx = X[j] - X[i]
                        dy = Y[j] - Y[i]

                        # Création d'un vecteur directeur normalisé
                        n = (dx*dx+dy*dy)**0.5
                        xx = dx / n
                        yy = dy / n

                        c = 0 # Cte pour le décalage de la flèche (0 par défaut)
                        # Si un lien existe dans l'autre sens, on décale la flèche pour éviter la superposition des deux flèches
                        if self.A[j][i] != inf:
                            c = 0.1

                        """
                        Création de la flèche
                        x : départ
                        rayon*xx : décalage lié à la taille du cercle
                        c*xx : décalage pour éviter la superposition des deux flèches
                        dx : arrivée
                        rayon*xx*2 : on retire deux fois la taille du cercle
                        """
                        arrow(x + rayon[i]*xx + c*yy,
                              y + rayon[i]*yy - c*xx,
                              dx - (rayon[i] + rayon[j])*xx,
                              dy - (rayon[i] + rayon[j])*yy,
                              zorder=-1, head_width=0.15, length_includes_head=True)

                        # Affichage de la valeur du lien
                        if capacite:
                            txt = str(self.F[i][j]) + "/" + str(self.C[i][j])
                        else:
                            txt = str(self.A[i][j])
                        text(x + dx / 2 + (0.2 + c)*yy, y + dy / 2 - (0.2 + c)*xx, txt, ha='center', va='center')

        # Affichage du nom des noeuds
        for i in range(0, l):
            text(X[i], Y[i], str(self.S[i]), ha='center', va='center')

    def position_noeuds(self, mode="random"):
        """
        Positionnement des noeuds de manière aléatoire
        :param mode: Mode de positionnement des noeuds
        """
        X = []
        Y = []
        l = len(self.S)

        if mode == "random":
            for i in range(0, l):
                while True:
                    x = randint(1, 10)
                    y = randint(1, 10)
                    if x not in X and y not in Y:
                        break
                X.append(x)
                Y.append(y)

        return X, Y

    def calcul_taille_noeuds(self, rmin=0.2, rmax=1.0, uniform=False):
        """
        Calcul la taille des noeuds
        :param rmin: rayon min
        :param rmax: rayon max
        :param uniform: même rayon pour chaque noeud
        :return: les rayons de chaque noeud
        """
        l = len(self.S)
        rayon = []

        if not uniform:
            C = []
            for i in range(0, l):
                c = 0 # Nombre de liens attachés au noeud
                for j in range(0, l):
                    if self.A[i][j] != inf:
                        c += 1
                    if self.A[j][i] != inf:
                        c += 1
                C.append(c)

            cmax = max(C)
            cmin = min(C)
            if cmax != cmin:
                for i in range(0, l):
                    rayon.append(rmin + (C[i] - cmin) / (cmax - cmin) * (rmax - rmin))
            else:
                rayon = [rmin for i in range(0, l)]
        else:
            rayon = [rmin for i in range(0, l)]

        return rayon

    def calcul_couleur_noeuds(self, mode="basique"):
        """
        Calcul la couleur de chaque noeud
        :param mode: mode d'assignement des couleurs
        :return: liste des couleurs
        """
        couleur = []

        if mode == "basique":
            couleur = ['b' for i in range(0, len(self.S))]

        return couleur

    def afficher(self, capacite=False):
        """
        Affiche le graphe en 2D
        :param capacite: Affichage de la capacité au lieu du poids des liens
        """

        fig = figure(figsize=(12, 12), dpi=80)
        ax = fig.add_subplot(111)

        # Positions des noeuds dans le graphe
        X, Y = self.position_noeuds()

        rayon = self.calcul_taille_noeuds(rmin=0.3, rmax=0.5)

        couleur = self.calcul_couleur_noeuds()

        self.plot(ax, rayon, couleur, X, Y, capacite)

        axis('scaled')
        show()
