""" Ce programme renomme tous les fichiers d'un répertoire passé en argument en enlevant les caractères spéciaux et en passant tout en minuscules. """

import os
import sys
import re

rep=sys.argv[1]
rep=re.sub('/$', '', rep)


for fichier in os.listdir(rep):
	fichpasext=re.sub('^(.+)\.([^\.]+)$', '\g<1>', fichier)
	ext=re.sub('^(.+)\.([^\.]+)$', '\g<2>', fichier)
	nomfich=re.sub('[^A-Za-z0-9_]', '_', fichpasext)
	nomfich=nomfich.lower()
	os.rename(rep+'/'+fichier, rep+'/'+nomfich+'.'+ext)
