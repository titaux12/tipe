from Réseau import *

def Dijkstra(graphe, s1, s2):
    """
    Algorithme de Dijkstra pour la recherche d'un plus court chemin entre deux sommets d'un graphe
    :param graphe: objet de type Reseau (graphe)
    :param s1: sommet de départ
    :param s2: sommet d'arrivé
    :return: le plus court chemin entre les deux sommets
    """

    assert isinstance(graphe, Reseau)
    assert isinstance(s1, str)
    assert isinstance(s2, str)

    S = graphe.S

    # On vérifie que l'ensemble des valuations des arcs sont positives
    l = len(graphe.A)
    for x in range(0, l):
        ligne = graphe.A[x]
        for y in range(0, l):
            a = ligne[y]
            if a < 0:
                print("La valuation de l'arc entre " + S[x] + " et " + S[y] + " est négative !")
                return None;

    # Initialisation de l'algorithme
    inf = float('inf')
    d = [] # Distance estimée de chaque sommet
    P = [None] * len(S) # Tableau des pères
    M = [] # Liste des sommets marqués
    min_dist = 0

    d = [inf] * len(S)
    d[S.index(s1)] = 0

    while min_dist != inf:

        for s in S:
            if d[S.index(s)] == min_dist and M.count(s) == 0:
                x = s
        M.append(x)
        for y in S:
            if M.count(y) == 0: # Si le sommet n'est pas marqué
                if d[S.index(x)] + graphe.v(x, y) < d[S.index(y)]:
                    d[S.index(y)] = d[S.index(x)] + graphe.v(x, y)
                    P[S.index(y)] = x
        min = inf
        for s in S:
            if M.count(s) == 0:
                if d[S.index(s)] < min:
                    min = d[S.index(s)]
        min_dist = min

    # Construction du chemin
    chemin = [s2]
    p = P[S.index(s2)]
    while p != None:
        chemin.append(p)
        p = P[S.index(p)]
    chemin.reverse()

    return chemin