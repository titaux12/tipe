from Réseau import *

inf = float('inf')

r = Reseau(
    ['A', 'B', 'C', 'D'],
    [
        [inf, inf, 6, 5],
        [2, inf, inf, 12],
        [inf, 3, inf, inf],
        [inf, inf, 1, inf]
    ],
    [
        [12, 8, 6, 2],
        [10, 5, 3, 3],
        [53, 3, 23, 1],
        [8, 5, 1, 12]
    ]
)

r.ajouter_noeud('E')
r.ajouter_lien('E', 'A', 12)
r.afficher()
