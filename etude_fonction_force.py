# coding: utf8

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

# Paramètres
F_max = 5000
F_min = 10000

h = 1.25 # Temps de sécurité
l = 4 # Longueur d'une voiture

n = F_max / 36 # Coefficient de frottement fictif
vitesse = 0 # Vitesse de la voiture de devant
d_securite = l + vitesse * h # Distance de sécurité

v = d_securite / h
d = l

def g(delta_v, delta_x):
    """
    Etude de la fonction qui permet de déterminer la force appliquée par le conducteur en fonction des différents paramètres
    :param delta_v: vitesse relative par rapport à la voiture de devant
    :param delta_x: distance relative par rapport à la voiture de devant
    :return: la force résultante appliquée par le conducteur
    """

    F = n*vitesse + (F_max - n*vitesse)*(1 - exp(-delta_v/v) * exp((d_securite - delta_x)/d))

    F = min(F, F_max)
    return max(F, -F_min)

def G(delta_v, delta_x):
    """
    Etude de la fonction qui permet de déterminer la force appliquée par le conducteur en fonction des différents paramètres
    :param delta_v: vitesse relative par rapport à la voiture de devant
    :param delta_x: distance relative par rapport à la voiture de devant
    :return: la force résultante appliquée par le conducteur
    """
    V = delta_v.tolist()[0]
    D = delta_x.tolist()
    R = []
    for d in D:
        d = d[0]
        R_temp = []
        for v in V:
            R_temp.append(g(v, d))
        R.append(R_temp)
    return R

def tracer(xmin, xmax, ymin, ymax):
    fig = figure()
    ax = fig.gca(projection='3d')
    X = np.arange(xmin, xmax+1, 1)
    Y = np.arange(ymin, ymax+1, 1)
    X, Y = np.meshgrid(X, Y)

    Z = G(X, Y)

    surf = ax.plot_surface(X, Y, Z, rstride=30, cstride=30, cmap=cm.coolwarm, linewidth=1)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_zlim(-F_min, F_max)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_xlabel("vitesse relative (m/s)")
    ax.set_ylabel("distance relative (m)")
    ax.set_zlabel("g(distance, vitesse)")

    show()

if __name__ == '__main__':
    tracer(vitesse - 36, vitesse, 0, 700)
