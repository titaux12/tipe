# coding: utf8

from pylab import *
from mpl_toolkits.mplot3d import Axes3D

# Paramètres
vitesse_limite = 36
distance_securite = 2 * vitesse_limite
vitesse_caracteristique = vitesse_limite

def g(delta_v, delta_h):
    """
    Etude de la fonction qui permet de déterminer la force appliquée par le conducteur en fonction des différents paramètres
    :param delta_v: vitesse relative par rapport à la voiture de devant
    :param delta_h: distance relative par rapport à la distance de sécurité
    :return: la force résultante appliquée par le conducteur
    """
    r = (np.arctan(1*(delta_h + 15*delta_v)/distance_securite)/np.pi + 0.5)*2 - 1
    return r

def tracer(xmin, xmax, ymin, ymax):
    fig = figure()
    ax = fig.gca(projection='3d')
    X = np.arange(xmin, xmax, 0.4)
    Y = np.arange(ymin, ymax, 0.4)
    X, Y = np.meshgrid(X, Y)

    surf = ax.plot_surface(X, Y, g(X, Y), rstride=30, cstride=30, cmap=cm.coolwarm, linewidth=1)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    ax.set_zlim(-1, 1)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_xlabel("vitesse relative (m/s)")
    ax.set_ylabel("distance relative (m)")
    ax.set_zlabel("g(distance, vitesse)")

    show()

if __name__ == '__main__':
    tracer(-vitesse_limite, vitesse_limite, -distance_securite, 500)