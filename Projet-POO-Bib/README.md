Bienvenue dans mon application !

[Lien] de référence de la bibliothèque de livres : https://math.univ-angers.fr/~jaclin/biblio/livres

Pour lancer l'algorithme de web scraping, taper dans la ligne de commande : 

" python3 main.py [Lien] [profondeur] "

Pour générer des rapports explicatifs des livres téléchargés (par auteur et par livre): 

"python3 main.py rapports [profondeur]"

L'utilisateur peut configurer le fichier "biblio.conf.txt" en ajustant les chemins des rapports qu'il veut générer et le nombre maximal de livres à télécharger et lancer l'application comme suit:

"python3 main.py -c bibli.conf.txt [Lien] [profondeur]"
