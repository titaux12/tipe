# coding: utf8

import numpy as np
import pylab as plt
from matplotlib import animation

"""
Résolution numérique de l'équation aux dérivées partielles:
    du/dx + df(u)/dt = 0
    u(x,0) = u0(x)
"""

# Paramètres de la simulation numérique
xmax = 20
tmax = 40
# Pas d'intégration
Dt = 0.1
Dx = 0.1

# Nombre de points de calcul
Nx = int(xmax // Dx) + 1
Nt = int(tmax // Dt) + 1

def f(u):
    """ Fonction f(u) de l'équation différentielle """
    return 0.5*u**2

def initialisation():
    """ Renvoie u0 la condition initiale du problème """
    t = gaussienne()
    return t

def bord(T, t):
    """ Conditions aux bords pour x=0 et x=xmax au temps d'intégration t """
    T[0, t] = 0
    T[-1, t] = 0
    return T


# Création de différentes fonctions u0 initales
def choc():
    """ Répartition constante égale à 1 puis nulle """
    t = np.zeros(Nx)
    for x in range(0, Nx//2):
        t[x] = 1
    return t

def gaussienne():
    """ Répartition gaussienne centrée en x=10 """
    return np.array([np.exp(-(x*Dx - 10)**2) for x in range(0, Nx)])


# Fonctions permettant l'affichage des résultats et leur sauvegarde
def afficher(T):
    """ Affichage simple de u(x, t) au temps t en fonction de x """
    X = np.arange(0, Nx) * Dx
    plt.plot(X, T)
    plt.show()

def afficher_2D(T):
    """ Affichage d'un graphique 2D permettant de visualiser l'évolution de u(x,t) en fonction du temps """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.imshow(T, origin='lower', interpolation='nearest', cmap=plt.cm.afmhot, aspect='auto', extent=[0, tmax, 0, xmax])
    plt.colorbar()
    plt.xlabel("Temps (s)")
    plt.ylabel("Position x (m)")
    plt.show()

def visualisation(T):
    """ Animation de u(x,t) en fonction du temps avec sauvegarde sous forme d'un fichier mp4 """
    fig = plt.figure()
    data, = plt.plot([], [])
    plt.xlim(0, xmax)
    plt.ylim(0, 1.5)

    X = np.arange(0, Nx) * Dx

    def update(k):
        Y = T[:, k]
        data.set_data(X, Y)
        # plt.title("Temps : " + str(round(Dt * k)) + "s")
        return data

    anim = animation.FuncAnimation(fig, update, frames=Nt, interval=Dt/1000, repeat=False)

    plt.legend()
    plt.show()

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30)

    # anim.save('Résultats/bouchon_01.mp4', writer=writer)


def resolution():
    T = np.zeros((Nx, Nt))
    u0 = initialisation()

    T[:,0] = u0

    for t in range(0, Nt-1):
        T = bord(T, t+1)
        for x in range(1, Nx-1):
            T[x, t+1] = 0.5*(T[x+1, t] + T[x-1, t]) - Dt*(f(T[x+1, t]) - f(T[x-1, t]))/(2*Dx)

    visualisation(T)
    afficher_2D(T)

resolution()
