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

    if delta_h < 0:
        return -1
    else:
        return 1

def G(delta_v, delta_h):
    """
    Etude de la fonction qui permet de déterminer la force appliquée par le conducteur en fonction des différents paramètres
    :param delta_v: vitesse relative par rapport à la voiture de devant
    :param delta_h: distance relative par rapport à la distance de sécurité
    :return: la force résultante appliquée par le conducteur
    """
    V = delta_v.tolist()[0]
    D = delta_h.tolist()
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

    ax.set_zlim(-1, 1)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_xlabel("vitesse relative (m/s)")
    ax.set_ylabel("distance relative (m)")
    ax.set_zlabel("g(distance, vitesse)")

    show()

if __name__ == '__main__':
    tracer(-vitesse_limite, vitesse_limite, -distance_securite, 700)
