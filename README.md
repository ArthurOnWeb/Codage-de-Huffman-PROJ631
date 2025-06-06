# Codage de Huffman

Ce dépôt contient une implémentation simple de l'algorithme de compression de Huffman en Python.

## Prérequis

- Python 3
- Le paquet `bitarray` (`pip install bitarray`)

## Utilisation

1. Placez dans le répertoire un fichier texte à compresser.
2. Lancez le script principal :
   ```bash
   python Main.py
   ```
3. Saisissez le nom du fichier lorsque le programme le demande.
4. Deux fichiers sont générés :
   - `<nom>_comp.bin` : le texte compressé au format binaire.
   - `<nom>_freq.txt` : les fréquences des caractères utilisées pour la décompression.

Le programme affiche également le taux de compression obtenu et le nombre moyen de bits nécessaires par caractère.

## Organisation du projet

- `Main.py` : script principal réalisant la compression et les statistiques.
- `Node.py` : définition de la structure d'arbre utilisée par l'algorithme.
- `textesimple.txt`, `extraitalice.txt`, `alice.txt` : exemples de textes à compresser.

## Licence

Projet fourni à titre éducatif sans garantie.
