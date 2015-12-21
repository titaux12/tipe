# coding: utf8

from Route import *

class Simulation(object):

    def __init__(self):
        self.temps = 5*60.0 # Durée de la simulation en secondes
        self.delta = 1/5.0 # Intervalle de temps entre chaque calcul
        self.route = Route(3000, 36, self.delta)

    def initialisation(self, espacement, vitesse):
        self.route.initialisation(espacement, vitesse)

    def parametres(self, flux, densite):
        if not flux:
            self.route.desactiver_flux()
        if not densite:
            self.route.desactiver_densite()

    def lancer(self):
        temps_total = 0
        p = 0 # Avancement de la simulation
        i = 0
<<<<<<< HEAD
        indice = 0
        while temps_total <= self.temps:            #Boucle principale
            self.route.update(temps_total, indice)
=======
        indice = 0 # Nombre de tours dans la boucle

        while temps_total <= self.temps: # Boucle principale du programme
            self.route.update(self.delta, temps_total, indice)
>>>>>>> axelsauvage/master
            indice += 1
            temps_total += self.delta
            i += self.delta / self.temps
            if i >= 0.01:
                p += 0.01
                i -= 0.01
                print("Avancement de la simulation : " + str(round(p*100)) + "%")
        print("Fin de la simulation")

<<<<<<< HEAD
        self.route.analyse_voitures()
        #self.route.animation()
        self.route.analyse_trafic()
=======
        """ Lancement des analyses """
        # self.route.analyse_voitures(nombre=1)
        # self.route.animation()
        # self.route.analyse_trafic()
        """ Fin des analyses """

        # Sauvegarde des données
        self.route.sauvegarde()
>>>>>>> axelsauvage/master

        print("Arrêt de la simulation")

s = Simulation()
<<<<<<< HEAD
s.route.sections[0]=[0,1000,25,2]
s.route.sections.append([0,500,14,2.5])
s.route.sections.append([0,300,9,1.5])
s.route.sections.append([0,400,25,2])
s.route.organise_sections()
s.lancer()
=======

for p in range(10, 1500, 50):
    s.initialisation(p, 0)
    s.lancer()
>>>>>>> axelsauvage/master
