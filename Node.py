class Node:
    def __init__(
        self,
        frequency,
        label=None,
        left_child=None,
        right_child=None,
    ) -> None:
        """Représente un nœud de l'arbre de Huffman.

        Args:
            frequency (int): fréquence d'apparition du caractère si c'est une
                feuille, somme des fréquences des deux fils sinon.
            label (str, optional): caractère contenu dans la feuille.
            left_child (Node, optional): fils de gauche.
            right_child (Node, optional): fils de droite.
        """
        self.frequency = frequency
        self.label = label
        self.left_child = left_child
        self.right_child = right_child

    def is_leaf(self):
        """Retourne ``True`` si le nœud est une feuille."""
        return self.left_child is None and self.right_child is None

    def parcours_profondeur(self, encodage=None):
        """Parcourt l'arbre en profondeur pour obtenir le code binaire des
        caractères.

        Args:
            encodage (list, optional): chemin parcouru sous forme de ``0`` ou
                ``1``. Defaults to ``None``.

        Returns:
            list: liste ``[caractère, fréquence, code_binaire]``
        """
        if encodage is None:
            encodage = []

        if self.is_leaf():
            result = encodage[:]
            return [[self.label, self.frequency, result]]

        gauche = []
        droite = []
        if self.left_child is not None:
            gauche = self.left_child.parcours_profondeur(encodage + [0])
        if self.right_child is not None:
            droite = self.right_child.parcours_profondeur(encodage + [1])
        return gauche + droite


def deuxpetits(liste_node) -> list:
    """on renvoie les deux plus petits noeuds d'une liste de noeuds

    Args:
        liste_node (list): liste de noeuds

    Returns:
        list: [plus_petit_noeud,plus_petit_noeud2]
    """
    plus_petit = liste_node[0]
    liste = liste_node.copy()
    for node in liste:
        if plus_petit.frequency > node.frequency:
            plus_petit = node
    liste.pop(liste.index(plus_petit))
    plus_petit2 = liste[0]
    for node in liste:
        if plus_petit2.frequency > node.frequency:
            plus_petit2 = node
    return [plus_petit, plus_petit2]


def creationarbre(liste_feuilles):
    """Permet de créer l'arbre à partir de ses feuilles en renvoyant sa racine

    Args:
        liste_feuilles (list): les feuilles de l'arbres

    Returns:
        list: une liste qui contient la racine de l'arbre
    """
    liste_travail = liste_feuilles.copy()
    if len(liste_travail) == 1:
        return liste_travail
    petits = deuxpetits(liste_travail)
    liste_travail.pop(liste_travail.index(petits[0]))
    liste_travail.pop(liste_travail.index(petits[1]))
    liste_travail += [Node(petits[0].frequency+petits[1].frequency,
                           left_child=petits[0], right_child=petits[1])]
    return creationarbre(liste_travail)
