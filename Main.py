from Node import *
from bitarray import bitarray
import os
import argparse


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
    # pour passer de octet/caractère à bit/caractère, il faut diviser par 8 le résultat
    bit_par_caractère = taillecompresse/length/8
    print(
        f'le nombre moyen de bit de stockage par caractère est : {bit_par_caractère} bits')

def compress(nom_fichier):
    """Compresse un fichier texte en utilisant l'algorithme de Huffman."""

    alphabet = alphabet_frequency(nom_fichier)
    liste_caracteres = list(alphabet.keys())

    liste_feuilles = [Node(alphabet[key], key) for key in liste_caracteres]
    arbre = creationarbre(liste_feuilles)[0]

    parcours_profondeur = arbre.parcours_profondeur()
    new_alphabet = {result[0]: list_to_string(result[2]) for result in parcours_profondeur}

    texte_compresse = text_to_bitarray(nom_fichier, new_alphabet)
    with open(nom_fichier[:-4] + '_comp.bin', 'wb') as new_file:
        texte_compresse.tofile(new_file)

    with open(nom_fichier, 'r') as f:
        reader = f.read()
        nb_caracteres = len(reader)
    with open(nom_fichier[:-4] + '_freq.txt', 'w') as new_file:
        new_file.write(f"{nb_caracteres}\n")
        for key in liste_caracteres:
            new_file.write(f"{key} {alphabet[key]}\n")

    compare_size(nom_fichier, nom_fichier[:-4] + '_comp.bin')

    nb_bits = sum(len(new_alphabet[key]) * alphabet[key] for key in liste_caracteres)
    nb_caracteres_total = sum(alphabet[key] for key in liste_caracteres)
    print(
        f"le nombre moyen de bits de stockage par caractères est : {nb_bits / nb_caracteres_total} bits")


def decompress(nom_fichier):
    """Recrée le texte original à partir des fichiers de compression."""

    if nom_fichier.endswith('.txt'):
        nom_fichier = nom_fichier[:-4]

    freq_file = nom_fichier + '_freq.txt'
    comp_file = nom_fichier + '_comp.bin'

    with open(freq_file, 'r') as f:
        lines = f.read().splitlines()

    nb_caracteres = int(lines[0])
    feuilles = []
    for line in lines[1:]:
        if not line:
            continue
        char = line[0]
        freq = int(line[2:])
        feuilles.append(Node(freq, char))

    arbre = creationarbre(feuilles)[0]

    bits = bitarray()
    with open(comp_file, 'rb') as f:
        bits.fromfile(f)

    decoded = []
    node = arbre
    for bit in bits:
        node = node.left_child if bit == 0 else node.right_child
        if node.is_leaf():
            decoded.append(node.label)
            if len(decoded) == nb_caracteres:
                break
            node = arbre

    output_file = nom_fichier + '_decomp.txt'
    with open(output_file, 'w') as f:
        f.write(''.join(decoded))
    print(f'Fichier d\xE9compress\xE9 \xE9crit dans {output_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compression et d\xE9compression Huffman')
    parser.add_argument('fichier', help='Fichier texte (pour la compression) ou nom de base (pour la d\xE9compression)')
    parser.add_argument('-d', '--decompress', action='store_true', help='D\xE9compresser le fichier sp\xE9cifi\xE9')
    args = parser.parse_args()

    if args.decompress:
        decompress(args.fichier)
    else:
        compress(args.fichier)
