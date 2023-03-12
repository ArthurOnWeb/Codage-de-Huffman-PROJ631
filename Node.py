class Node:
    def __init__(self, frequency, label=None, left_child=None, right_child=None) -> None:
        """Un noeud contient la fréquence d'apparition du caractère qu'il représente si c'est une feuille sinon, l'addtition de la fréquence d'apparition de ses deux fils

        Args:
            frequency (int): la fréquence d'apparition du caractère si c'est une feuille, la somme de celle de ses deux fils sinon
            label (string, optional): caractère contenu dans la feuille. Defaults to None.
            left_child (Node, optional): le fils de gauche. Defaults to None.
            right_child (Node, optional): le fils de droite. Defaults to None.
        """
        self.frequency = frequency
        self.label = label
        self.left_child = left_child
        self.right_child = right_child

    def is_leaf(self):
        """vérifies si le noeud est une feuill

        Returns:
            Bool: True si c'est une feuille, False sinon
        """
        if self.left_child == None and self.right_child == None:
            return True
        else:
            return False

    def parcours_profondeur(self, encodage=[]):
        """Parcours l'arbre en profondeur afin de renvoyer la représentation binaire de chaque caractères

        Args:
            encodage (list, optional): permet de garder en mémoire le chemin parcourue sous forme de 0 et de 1. Defaults to [].

        Returns:
            list: Une liste de liste contenant le caractère, sa fréquence ainsi que sa représentation en binaire
        """
        if self.is_leaf() == True:
            result = encodage[:]
            return [[self.label, self.frequency, result]]
        gauche = []
        droite = []
        if self.left_child != None:
            encodage += [0]
            gauche = self.left_child.parcours_profondeur(encodage)
            encodage.pop()
        if self.right_child != None:
            encodage += [1]
            droite = self.right_child.parcours_profondeur(encodage)
            encodage.pop()
        # return [encodage[:]+[self.frequency]]+gauche+droite
        return gauche+droite
