# Codage de Huffman

Ce dépôt contient une implémentation simple de l'algorithme de compression de Huffman en Python.

## Prérequis

- Python 3
- Le paquet `bitarray` (`pip install bitarray`)

## Utilisation

1. Placez dans le répertoire un fichier texte à compresser.
2. Lancez la compression :
   ```bash
   python Main.py monfichier.txt
   ```
   Deux fichiers sont générés :
   - `<nom>_comp.bin` : le texte compressé au format binaire.
   - `<nom>_freq.txt` : les fréquences des caractères utilisées pour la décompression.

3. Pour retrouver le texte d'origine :
   ```bash
   python Main.py -d monfichier
   ```
   Le fichier `<nom>_decomp.txt` est alors créé.

Le programme affiche également le taux de compression obtenu et le nombre moyen de bits nécessaires par caractère.

## Organisation du projet

- `Main.py` : script principal réalisant la compression et les statistiques.
- `Node.py` : définition de la structure d'arbre utilisée par l'algorithme.
- `textesimple.txt`, `extraitalice.txt`, `alice.txt` : exemples de textes à compresser.

## Licence

Projet fourni à titre éducatif sans garantie.
