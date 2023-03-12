from Node import Node
from bitarray import bitarray
import os


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


def alphabet_frequency(nom_fichier) -> dict:
    """Renvoies un dictionnaire comportant les caractères du texte dans l'ordre de fréquence croissante puis si deux caractères ont le même nombre d'apparition, par leur ordre dans l'alphabet ASCII

    Args:
        nom_fichier (string): fichier qui contient le texte

    Returns:
        dict: {"caractère":fréquence,....}
    """
    with open(nom_fichier, 'r') as f:
        reader = f.read()
    alphabet = dict()
    for caractere in reader:
        try:
            alphabet[caractere] += 1
        except:
            alphabet[caractere] = 1
    alphabet_tri = dict(sorted(alphabet.items(), key=lambda x: x[0]))
    alphabet_tri = dict(sorted(alphabet_tri.items(), key=lambda x: x[1]))
    return alphabet_tri


def list_to_string(liste):
    """Transforme une liste en une chaine de caractères

    Args:
        liste (list): la liste à transformer

    Returns:
        string: les caractères de la liste sous forme de chaîne de caractère
    """
    result = ''
    for chiffre in liste:
        result += f"{chiffre}"
    return result


def text_to_bitarray(nom_fichier, binary_dict):
    """transforme un text en une suite de bits

    Args:
        nom_fichier (string): le nom du fichier
        binary_dict (dict): le dictionnaire qui contient la correspondance entre le caractère brut et le caractère en binaire

    Returns:
        bitarray: une suite de bits qui représente le texte
    """
    with open(nom_fichier, 'r') as f:
        reader = f.read()
    string_list = []
    for char in reader:
        string_list += [binary_dict[char]]
    bit_list = []
    for str in string_list:
        for bit in str:
            bit_list += [int(bit)]
    bits = bitarray(bit_list)
    return bits


def compare_size(fichierbase, fichiercompresse):
    """calcule le taux de compression

    Args:
        fichierbase (string): le fichier de base
        fichiercompresse (string): le fichier compressé
    """
    taillebase = os.path.getsize(fichierbase)
    taillecompresse = os.path.getsize(fichiercompresse)
    taux_compression = 1-taillecompresse/taillebase
    print(f'le taux de compression est de {taux_compression}')


def lengthonbit(fichierbase, fichiercompresse):
    """calcule le nombre de bit par caractère

    Args:
        fichierbase (string): le fichier de base
        fichiercompresse (string): le fichier compressé
    """
    with open(fichierbase, 'r') as f:
        reader = f.read()
    length = len(reader)
    taillecompresse = os.path.getsize(fichiercompresse)
    bit_par_caractère = taillecompresse/length
    print(
        f'le nombre moyen de bit de stockage par caractère est : {bit_par_caractère}')


if __name__ == '__main__':

    # 1. création du dictionnaires avec les caractères et leurs fréquences

    nom_fichier = 'extraitalice.txt'
    alphabet = alphabet_frequency(nom_fichier)
    liste_caracteres = alphabet.keys()

    # 2. création de l'arbre

    # je créer les feuilles de mon arbre
    liste_feuilles = []
    for key in liste_caracteres:
        liste_feuilles += [Node(alphabet[key], key)]

    # je créer l'arbre de Huffman
    arbre = creationarbre(liste_feuilles)[0]

    # 3. Codage du texte

    # je parcours l'arbre en profondeur pour récupérer la représentation en binaire de chaque caractère
    parcours_profondeur = arbre.parcours_profondeur()

    # je créer le dictionnaire qui lie caractère et représentation en binaire
    new_alphabet = dict()
    for result in parcours_profondeur:
        new_alphabet[result[0]] = list_to_string(result[2])

    # je créer le fichier qui contient le texte compressé
    texte_compresse = text_to_bitarray(nom_fichier, new_alphabet)
    with open(nom_fichier[:-4]+'_comp.bin', mode='wb',) as new_file:
        texte_compresse.tofile(new_file)

    # je créer le fichier qui va contenir le dictionnaire contenant l'alphabet ainsi que les fréquences d'apparition des caractères

    with open(nom_fichier, mode='r') as f:
        reader = f.read()
        nb_caracteres = len(reader)
    with open(nom_fichier[:-4]+'_freq.txt', mode='w') as new_file:
        new_file.write(f'{nb_caracteres}\n')
        keys = alphabet.keys()
        for key in keys:
            new_file.write(f'{key} {alphabet[key]}\n')

    # 4. Détermination du taux de compression

    compare_size(nom_fichier, nom_fichier[:-4]+'_comp.bin')

    # 5. Détermination du nombre moyen de bits de stockage d’un caractère du texte compressé

    lengthonbit(nom_fichier, nom_fichier[:-4]+'_comp.bin')
