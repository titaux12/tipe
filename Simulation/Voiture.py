# coding: utf8

from etude_fonction_force import g


class Voiture(object):

    def __init__(self, position, vitesse):
        assert position >= 0
        assert vitesse >= 0
        # Vitesse et position initiales de la voiture
        self.position = position # position en mètre
        self.vitesse = vitesse # vitesse en m/s

        self.donnees = []
        self.masse = 1300 # masse en kg
        self.longueur = 4 # longueur en mètre
        self.F_max = 3000 # Force d'accélération maximum
        self.F_min = 3000 # Force de freinage maximum

    def update(self, temps_total, delta, voiture_derriere, voiture_devant, vitesse_limite, distance_securite):
        # Influence de la voiture de devant
        if voiture_devant is not None:
            # Distance relative par rapport à la voiture de devant
            delta_h = (voiture_devant.position - self.position) - distance_securite
            # Vitesse relative avec la voiture de devant
            delta_v = voiture_devant.vitesse - self.vitesse
        else:
            delta_h = 10000
            delta_v = 10000

        # Calcul de la force appliquée par le conducteur
        G = g(delta_v, delta_h)

        if G > 0:
            G *= self.F_max
        else:
            G *= self.F_min

        n = self.F_max / vitesse_limite

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
                F
            ]
        ])

    def obtenir_positions(self):
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][0])
        return t, r

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
