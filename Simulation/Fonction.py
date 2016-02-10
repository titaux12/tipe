# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 07:59:16 2016

@author: louismelchior
"""
from pylab import *
from math import *

class Fonction(object):
    """Class Fonction : 
    -Initialisation : Rentrer fct en fonction de x ! (string)
    -Fct : nécessairement positive ou nul sur [0,distance]
    -Distance : Longeur de l'intervalle
    -Pas : Déconseiller de le changer après tableau
    """
    def __init__(self,FCT,pas=0.1,mini=4):
        self.FCT=FCT    #[["f(x)",longueur]...]
        self.distance=0        
        for i in range(len(FCT)):
            self.distance+= FCT[i][1]
        self.pas=pas
        self.X=[]   #Découpage de l'interval
        self.Y=[]   #Valeur de la fonction
        self.entite=[]        #[[nombre d'entite,position en m],...]
        self.mini=mini  #Distance minimale à respecter entre entités
        self.E=[]   #Nombre d'entités à P à indices identiques
        self.P=[]   #Position des E à indices identiques
        self.F=[]   #Position des entités (1 par position)
        self.N=0    #Nombre d'entité
        
    def initialisation(self,R=0):
        self.X,self.Y=self.tableau()
        if R:
            self.entite=self.repartition()
    
    def fonction(self,d):
        x=d
        i=0
        while d - self.FCT[i][1]>0:
            d-=self.FCT[i][1]
            i+=1
        y=eval(self.FCT[i][0])
        return y
    
    def tableau(self):  #Crée la representation de la fonction
        X=np.linspace(0,self.distance,self.distance//self.pas)
        Y=[self.fonction(x) for x in X] 
        return X,Y
    
    def repartition(self):
        """ Requiert une initialisation préalable
            Méthode : airs des rectangles à gauche:
            -seg = base des rectangles
            Important : Aux vues des longueur mise en jeu dans Simulation, le pas=seg doit convenir !
                        En d'autre termes, il faudra veiller a avoir des fonctions respectant au moins 
                        la longeur des voitures.
            return : Liste double contenant le nombre de voiture et leur position
        """
        entite=[]       #Liste contenant 
        seg=self.pas    #base des rectangles
        air=0
        Max=0           #Plus grande variation du nombre de voiture dans une section
        for i in range(0,len(self.X)):   #Tant que l'intervalle n'est pas balayé
            air+=seg*self.Y[i]
            if int(air)>Max: #Mise a jour du Max rectangle
                Max=int(air)
            entite.append([int(air),self.X[i]]) #Place (int(air)) entite a la position X[i]
            air-=int(air)
        return entite   #[[entite,position en m],...]
        
    def affiche(self):
        plot(self.X,self.Y)    
        show()

    def analyse_rep(self):
        Min=self.distance   #Initialisation min
        entite=self.entite
        if not len(self.entite):
            entite=self.repartition()
        j=0 #Première position
        while not entite[j][0]:     #On parcourt entite tant que pas de voiture
            j+=1
        x=entite[j][1]
        for i in range(j+1,len(entite)):
            if entite[i][0]:    #Si il y a une entite a l'indice i
                if entite[i][1] - x < Min:
                    Min= entite[i][1] - x
                x=entite[i][1]
        return Min
    
    def credible(self):
        if not self.entite:
            self.initialisation(1)
        if not self.E:
            self.rep_ent()
        if min(self.Y)<0:
            return False
        if self.mini < self.analyse_rep() and max(self.E)==1:
            return True
        else:
            return False
    
    def position(self):
        if not self.entite:
            self.initialisation(1)
        if not self.E:
            self.rep_ent()
        if self.credible():
            for i in range(len(self.E)):
                if self.E[i]:   #Si il y a une voiture
                    self.F+=[self.P[i]]     #Ajoute la position de cette voiture
            return self.F
        else:
            return False    #Renvoie False si pas credible
    
    def rep_ent(self):
        for i in range(len(self.entite)):
            self.E+=[self.entite[i][0]]
            self.P+=[self.entite[i][1]]
        self.N=sum(self.E)
    
    
def affichage(X,Y):
    plot(X,Y)
    show()

def montre(X):
    for i in range(len(X)):
        print(X[i])
