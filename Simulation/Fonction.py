# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 07:59:16 2016

@author: louismelchior
"""

class Fonction(object):
    """Class Fonction : 
    -Initialisation : Rentrer fct en fonction de x !
    -Fct : nécessairement positive ou nul sur [0,distance]
    -Distance : Longeur de l'intervalle
    -Pas : Déconseiller de le changer après tableau
    """
    def __init__(self,fct,distance,pas=0.1):
        self.fct=fct
        self.distance=distance
        self.pas=pas
        self.X=[]        
        self.Y=[]        
        
    def initialisation(self):
        self.X,self.Y=self.tableau()
    
    def fonction(self,x):
        x=x
        y=eval(self.fct)
        return y
    
    def tableau(self):  #Crée la representation de la fonction
        X=[x for x in range(0,self.distance,self.pas)]
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
            entite.append(int(air),i) #Place (int(air)) entite a la position X[i]
            air-=int(air)
        return entite
    
    def analyse_rep(self):
        Min=self.distance
        entite=self.repartition()
        j=0 #Première position
        while not entite[j][0]:
            j+=1
        x=entite[j][1]  #Economie d'une variable avec x
        for i in range(j+1,len(entite)):
            if entite[i][0]:    #Si il y a une entite a l'indice i
                if x - entite[i][1]<Min:
                    Min= x - entite[i][1]
                x=entite[i][1]
        return Min