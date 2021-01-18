# AlgorithmiqueAppliquee

Projet d'algorithmique appliquée du M2 informatique fondamentale de Bordeaux proposé par Ludovic Hofer et Cyril Gavoille.

Le code n'est pas fini (notamment il n'est pas commenté par endroit). Ce n'est qu'une version préliminaire
du code final.

# Dépendances

## Documentation

Installer sphinx:

`pip install Sphinx`

Insaller le thème utilisé:

`pip install sphinx_rtd_theme`

# Utilisation

## Documentation

Pour générer la doc, il faut se placer à la racine du projet et utiliser la commande:

`make doc`

La documentation générée sera placée dans le dossier doc/.

## Basique

Pour le tester:

`python3 main.py <file> <solveur>`

où file est l'emplacement d'un problème à résoudre
et solveur le solveur à utiliser (greedy, random ou brute).

Le résultat du programme sera stocké dans src/data.json par défaut.

## Avec le visualiseur (Linux seulement)

Autoriser l'utilisation du script:

`chmod +x solve.sh`

Lancer le solveur sur un problème donné, puis ouvrir le visualiseur:

`./solve.sh <file> <solveur>`

## Le solveur random

Les paramètres des solveurs peuvent être modifiés dans le fichier `main.py` (dans la partie variable).

# Remerciement

Le code du visualiseur peut être trouvé [ici](https://www.labri.fr/perso/lhofer/index.php?page=teaching/algorithmique_appliquee/index).

Le code est sous licence MIT.