 # coding: utf8

from Route import *

class Simulation(object):

    def __init__(self,FCT):
        self.temps = 8*60.0 # Durée de la simulation en secondes
        self.fct=Fonction(FCT)
        self.delta = 1/5.0 # Intervalle de temps entre chaque calcul
        self.route = Route(3000, 36, self.delta,FCT)

    def initialisation(self):
        self.route.initialisation()

    def parametres(self, flux, densite):
        if not flux:
            self.route.desactiver_flux()
        if not densite:
            self.route.desactiver_densite()

    def lancer(self):

        if len(self.route.sections) == 0:
            print("Il faut au moins une section !")
            return None

        if not self.fct.credible(): #Les conditions initiales doivent être valides
            print("Répartition initiale invalide")
            return None
        if self.route.longueur < max(self.fct.position()):
            print("Répartition initiale invalide (voiture en dehors de la route)")
            return None

        temps_total = 0
        p = 0 # Avancement de la simulation
        i = 0
        indice = 0 # Nombre de tours dans la boucle

        while temps_total <= self.temps: # Boucle principale du programme
            self.route.update(self.delta, temps_total, indice)
            indice += 1
            temps_total += self.delta
            i += self.delta / self.temps
            if i >= 0.01:
                p += 0.01
                i -= 0.01
                print("Avancement de la simulation : " + str(round(p*100)) + "%")
        print("Fin de la simulation")
        print("Nombre de voiture dans la simulation",s.route.N)

        """ Lancement des analyses """
        self.route.analyse_voitures(nombre=-1)
        #self.route.animation()
        # self.route.analyse_trafic()
        """ Fin des analyses """

        # Sauvegarde des données
        # self.route.sauvegarde()

        print("Arrêt de la simulation")

s = Simulation([["0.02",100],["0",100],["0.05",100]])

s.route.ajouter_section(200, 30, 2)
s.route.ajouter_section(500, 10, 1.5)
s.route.ajouter_section(1000, 25, 2)
s.route.affichage_section()

s.initialisation()
s.lancer()

# for p in range(10, 1500, 50):
#     s.initialisation(p, 0)
#     s.lancer()
