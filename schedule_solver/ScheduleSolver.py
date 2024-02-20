from typing import Optional
from pulp import LpProblem, LpVariable, lpSum
from pulp.constants import LpMaximize, LpBinary


class ScheduleSolver(LpProblem):
    """
    Solveur d'emploi du temps basé sur pulp.LpProblem
    Permet d'attribuer des créneaux à un ensemble de nageurs
    en fonction de leurs disponibilités
    On cherche à maximiser le nombre de créneaux alloués
    """

    def __init__(
        self,
        free_swims_slots: list[tuple[int, int]],
        max_slots_per_swim: int | list[int] = 1,
        max_swims_per_slot: int | list[int] = 1,
        max_sum_races: Optional[int] = None,
    ):
        """
        Instancie un nouveau solveur à partir des disponibilités des nageurs

        :param free_swims_slots:
            Liste de tuples des disponibilités de chaque nageur de la forme [(i,j),...]
            Le nombre d'éléments correspond au nombre de variables du modèle
            Si (i,j) est dans la liste alors le nageur i est disponible pour le créneau j
            Les indices commencent à partir de 0
        :param max_slots_per_swim:
            Nombre maximum de créneaux autorisés par nageur
            Si c'est un entier la contrainte est appliquée indiféremment pour chaque nageur
            Si c'est une liste la contrainte est appliquée spécifiquement en fonction du nageur
        :param max_swims_per_slot:
            Nombre maximum de nageurs autorisés sur un même créneau
            Si c'est un entier la contrainte est appliquée indiféremment pour chaque créneau
            Si c'est une liste la contrainte est appliquée spécifiquement en fonction du créneau
        :param max_sum_races:
            Somme maximale autorisée de toutes les courses réalisées
            permettant de borner la fonction objectif
            Cette option est surtout utile si max_swimmers_per_slot > 1
            Si None pas de contrainte appliquée
        """
        # Vérification et prétraitement des entrées
        assert 0 < len(free_swims_slots)
        # Suppression des dupliqués et amélioration de la recherche
        free_swims_slots = set(free_swims_slots)
        n_swims = 1  # Nombre de nageurs
        n_slots = 1  # Nombre de créneaux
        for i, j in free_swims_slots:
            assert 0 <= i and 0 <= j
            n_swims = max(n_swims, i + 1)
            n_slots = max(n_slots, j + 1)
        # Nombre maximum de variables
        max_vars = n_swims * n_slots
        assert len(free_swims_slots) <= max_vars
        r_swims = range(n_swims)
        r_slots = range(n_slots)

        if isinstance(max_slots_per_swim, int):
            max_slots_per_swim = [max_slots_per_swim] * n_swims
        assert (
            isinstance(max_slots_per_swim, list) and len(max_slots_per_swim) == n_swims
        )

        if isinstance(max_swims_per_slot, int):
            max_swims_per_slot = [max_swims_per_slot] * n_slots
        assert (
            isinstance(max_swims_per_slot, list) and len(max_swims_per_slot) == n_slots
        )

        assert max_sum_races is None or 0 <= max_sum_races <= max_vars

        # Création du modèle
        super().__init__(name=self.__class__.__name__, sense=LpMaximize)

        # Si x[i,j] == 1 alors le nageur i est inscrit au créneau j
        x = LpVariable.dicts("x", free_swims_slots, cat=LpBinary)
        self.variables_swim_slot = x

        # Fonction objectif : on cherche à maximiser le nombre de créneaux alloués
        self += (
            lpSum([x[i, j] for (i, j) in free_swims_slots]),
            "sum_of_allocated_slots",
        )

        # Chaque nageur ne doit être inscrit que sur max_slots_per_swimmer créneau(x) au plus
        for i in r_swims:
            self += (
                lpSum([x[i, j] for j in r_slots if (i, j) in free_swims_slots])
                <= max_slots_per_swim[i],
                f"max slots {max_slots_per_swim[i]} for swimmer {i}",
            )

        # Chaque créneau ne peut être accordé au plus qu'à max_swimmers_per_slot nageur(s)
        for j in r_slots:
            self += (
                lpSum([x[i, j] for i in r_swims if (i, j) in free_swims_slots])
                <= max_swims_per_slot[j],
                f"max swimmers {max_swims_per_slot[j]} for slot {j}",
            )

        # On ne peut pas dépasser max_sum_races courses allouées
        if max_sum_races is not None:
            self += (
                lpSum(
                    [
                        x[i, j]
                        for i in r_swims
                        for j in r_slots
                        if (i, j) in free_swims_slots
                    ]
                )
                <= max_sum_races,
                f"max sum races {max_sum_races}",
            )
