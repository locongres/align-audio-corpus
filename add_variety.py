""" Ce programme ajoute une colonne contenant la variété indiquée en argument 2 à tous les fichiers csv d'un répertoire passé en argument 1. """


import sys
import re
import os


entree=sys.argv[1]
entree=re.sub('/$', '', entree)

var=sys.argv[2]


for fichier in os.listdir(entree):
	if re.search('\.csv$', fichier):
		nomfich=re.sub('\.csv$', '', fichier)
		nvfich=open(entree+'/'+nomfich+'_var.csv', 'w')
		nvfich.close()
		
		ancfich=open(entree+'/'+fichier, 'r')
		for ligne in ancfich:
			ligne=ligne.rstrip('\n')
			ligne=ligne+'§'+var
			nvfich=open(entree+'/'+nomfich+'_var.csv', 'a')
			nvfich.write(ligne+'\n')
			nvfich.close()
			
