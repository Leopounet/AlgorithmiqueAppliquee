# AlgorithmiqueAppliquee

Projet d'algorithmique appliquée du M2 informatique fondamentale de Bordeaux proposé par Ludovic Hofer et Cyril Gavoille.

Le code n'est pas fini (notamment il n'est pas commenté par endroit). Ce n'est qu'une version préliminaire
du code final.

# Utilisation

## Doc

Pour générer la doc, il faut se placer à la racine du projet et utiliser la commande:

`make doc`

La documentation générée sera placée dans le dossier doc/.

## Basique

Pour le tester:

`python3 test.py <file> <solveur>`

où file est l'emplacement d'un problème à résoudre
et solveur le solveur à utiliser (greedy, random ou brute).

Le résultat du programme sera stocké dans src/data.json par défaut.

## Avec le visualiseur (Linux seulement)

Autoriser l'utilisation du script:

`chmod +x run.sh`

Lancer le solveur sur un problème donné, puis ouvrir le visualiseur:

`./run.sh <file> <solveur>`

## Le solveur random

Les paramètres du solveur random peuvent être modifiés dans le fichier `test.py` (dans la partie variable). Les autres
solveurs n'ont pas de paramètres intéressants à modifier.

# Remerciement

Le code du visualiseur peut être trouvé [ici](https://www.labri.fr/perso/lhofer/index.php?page=teaching/algorithmique_appliquee/index).

Le code est sous licence MIT.