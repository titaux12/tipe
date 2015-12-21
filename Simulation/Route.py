# coding: utf8

from Voiture import *
from pylab import *
from matplotlib import animation


class Route(object):
    """
    Classe repesentant une route a plusieurs voies de circulation.
    """

    def __init__(self, longueur = 3000, vitesse_limite = 36):
        self.longueur = longueur # Longueur de la route en metre
        self.vitesse_limite = vitesse_limite # Vitesse maximale autorisee en m/s
        self.temps_securite = 2

        self.voitures_valides = [] # Liste contenant les voitures valides
                                   #Est ce classer dans un ordre particulier ?
        self.voitures = [] # Liste contenant les voitures
        self.N_tot = 0 # Nombre de voitures sur la route
        self.N = 0 # Nombre de voitures sur la route valides
        self.sections=[ #[position, longueur, Vmax, temps_securite]
                        #Etat initial : 1 section = la route
        [0,self.longueur,self.vitesse_limite,self.temps_securite]        
        ]        
        
        
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []
        self.temps_total = 0 # Temps total de la simulation
        self.pas = 50 # Pas de mesure pour le flux et la densite
        self.timer = 0 
        self.frequence = 1 #Frequence d'apparation de nouvelle voiture
        self.f_max = 50
        self.f_min = 1/10
        self.delta = 0 #Intervalle de temps de simulation
        self.temps_max_generation=0        

    def initialisation(self, delta):
        self.voitures_valides = []
        self.voitures = []
        self.N = 0
        self.N_tot = 0
        self.flux = []
        self.densite = []
        self.temps_total = 0
        self.delta = delta
        self.temps_max_generation=self.sections[0][1] // self.sections[0][2]

    def affichage_section(self):
        n=1
        for section in self.sections :
            print("Section n°",n)
            n+=1
            print("Debut a:",section[0]," de longeur :",section[1]," vitesse maximal :"
            ,section[2]," et temps de securite :",section[3])
        print("Rappel du prototype d'ajout de section")
        print("S=[Debut,longueur,vitesse_limite,temps_securite]")

    def organise_sections(self):
        """
        Reorganise les sections : colle les sections les une contre les autres;
        A effectuer apres chaque supression de section
        Permet l'insertion de sections entre des sections deja existante"""
                
        assert len(self.sections)>1
        self.longueur=self.sections[0][1]
        self.temps_max_generation=self.sections[0][1] // self.sections[0][2]
        for i in range(1,len(self.sections)):
            self.sections[i][0] = self.sections[i-1][0] + self.sections[i-1][1] #Ajuste le debut des sections
            self.longueur+=self.sections[i][1] # Met a jour la distance total de la route
            self.temps_max_generation += self.sections[i][1] // self.sections[i][2]
        
    def numero_section(self,position):
        """Renvoi l'indice de section dans laquel la voiture ce situe"""
        if position>self.longueur: # Si la voiture est en dehors de la route
            return 0 # renvoie la 1ère section
        for i in range(len(self.sections)): # Parcours les sections
            position-=self.sections[i][1]
            if position<=0: # Privilegie la section la plus eloigne
            # Si position est dans sections[i]
                return i
        return 0
        

    
    def update(self, temps_total, indice):
        self.timer += self.delta
        if self.timer >= 1/self.frequence and temps_total <= self.temps_max_generation:
            if self.voitures_valides != []:
                voiture_devant = self.voitures_valides[0]
                if voiture_devant.position >= self.temps_securite * voiture_devant.vitesse + voiture_devant.longueur:
                    self.timer -= 1/self.frequence

                    self.frequence += 0.0

                    v = voiture_devant.vitesse
                    self.ajouter_voiture(0, v)
                else:
                    self.timer -= self.delta
            else:
                self.ajouter_voiture(0, 36)
                self.timer -= 1/self.frequence

        self.temps_total = temps_total
        for voiture in self.voitures_valides:
            if voiture.valide:
                i = self.voitures_valides.index(voiture)
                if i != self.N-1:
                    voiture_devant = self.voitures_valides[i+1]
                else:
                    if self.N > 0:
                        voiture_devant = self.voitures_valides[0]
                    else:
                        voiture_devant = None
                #Mise a jour de la voiture
                indice_section = self.numero_section(voiture.position)
                voiture.update(temps_total, self.delta, indice, voiture_devant,
                               self.longueur, self.sections[indice_section][3], self.sections[indice_section][2])

        #for voiture in self.voitures_valides:
            #if not voiture.valide:
                #self.retirer_voiture(voiture)

        # Mise a jour du flux de voitures
        F = []
        for k in range(0, self.longueur, self.pas):
            v_totale = 0
            for voiture in self.voitures_valides:
                if voiture.position >= k and voiture.position < k + self.pas and voiture.valide:
                    v_totale += voiture.vitesse
            F.append(v_totale / self.pas)

        self.flux.append([
            temps_total,
            F
        ])

        v = 0
        for voiture in self.voitures_valides:
            if voiture.valide:
                v += voiture.vitesse
        self.flux_total.append([
            temps_total,
            v / self.longueur
        ])

        # Mise a jour de la densite du trafic
        D = []
        for k in range(0, self.longueur, self.pas):
            v_totale = 0
            for voiture in self.voitures_valides:
                if abs(voiture.position - k) < self.pas and voiture.valide:
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
            print("Erreur ! Impossible de recuperer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_positions()
        plot(Y, X)

    def afficher_vitesse(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de recuperer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_vitesses()
        plot(X, Y)

    def afficher_force(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de recuperer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_forces()
        plot(X, Y)

    def afficher_distance(self, i1, i2):
        try:
            voiture1 = self.voitures[i1]
            voiture2 = self.voitures[i2]
        except:
            print("Erreur ! Impossible de recuperer les voitures d'indices " + str(i1) + " et " + str(i2))
            return None
        X, Y1 = voiture1.obtenir_positions()
        X, Y2 = voiture2.obtenir_positions()
        Y = []
        D = []
        for i in range(len(Y2)-1):
            Y.append(Y2[i] - Y1[i])
            #D.append(self.distance_securite)
        while len(X) != len(Y):
            X.pop(i)
        plot(X,Y)
        #label="Distance entre " + str(i1) + " et " + str(i2)

    def afficher(self, xmin, xmax, ymin, ymax):
        xlim(xmin, xmax)
        ylim(ymin, ymax)
        legend(loc="best")
        show()

    def analyse_voitures(self):
        print("Analyse des positions...")
        for i in range(self.N_tot): # Balai l'ensemble des voitures
            self.afficher_position(i)
        self.afficher(0, self.longueur, 0, self.temps_total)

        print("Analyse des distances relatives...")
        for i in range(self.N_tot - 1): # Balai l'ensemble des voitures
            self.afficher_distance(i,i+1)
        self.afficher(0, self.longueur, 0, self.temps_total)
        

        print("Analyse des vitesses...")
        for i in range(self.N_tot):
            self.afficher_vitesse(i)
        self.afficher(0, self.temps_total, 0, 40)

        print("Analyse des forces...")
        for i in range(self.N_tot):
            self.afficher_force(i)
        self.afficher(0, self.temps_total, -10000, 10000)

    def analyse_trafic(self):
        print("Analyse du flux...")
        self.afficher_flux()

        print("Analyse de la densite...")
        self.afficher_densite()

        print("Generation de la courbe flux-densite...")
        self.afficher_flux_densite()

    def animation(self):

        positions = []
        for voiture in self.voitures:
            positions.append(voiture.obtenir_positions(temps=False))

        fig = figure()
        data = plot([], [], 'bo')
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