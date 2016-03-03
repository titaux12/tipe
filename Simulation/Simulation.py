 # coding: utf8

from Route import *

class Simulation(object):

    def __init__(self):
        self.temps = 5*60.0 # Durée de la simulation en secondes
        self.delta = 1/5.0 # Intervalle de temps entre chaque calcul
        self.route = Route(3000, 36, self.delta,[["sin(x-1500)**2/2",1000]])

    def initialisation(self, espacement, vitesse):
        self.route.initialisation(espacement, vitesse)

    def parametres(self, flux, densite):
        if not flux:
            self.route.desactiver_flux()
        if not densite:
            self.route.desactiver_densite()

    def lancer(self):

        if len(self.route.sections) == 0:
            print("Il faut au moins une section !")
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

        """ Lancement des analyses """
        self.route.analyse_voitures(nombre=5)
        #self.route.animation()
        # self.route.analyse_trafic()
        """ Fin des analyses """

        # Sauvegarde des données
        # self.route.sauvegarde()

        print("Arrêt de la simulation")

s = Simulation()

s.route.ajouter_section(200, 25, 2)
s.route.ajouter_section(1000, 5, 2)
s.route.ajouter_section(2000, 25, 2)
s.route.affichage_section()

s.initialisation()
s.lancer()

# for p in range(10, 1500, 50):
#     s.initialisation(p, 0)
#     s.lancer()
