""" Ce programme essaie de récupérer la variété de phrases se trouvant dans un fichier de correspondance généré par le programme decoupefichrep.py. Pour chaque fichier nom_du_fichier_nv.csv contenu dans le répertoire passé en argument, il cherche un fichier exports/nom_du_fichier_corresp.csv et, pour chaque ligne de celui-ci attribue à la phrase la variété indiquée pour celle-ci dans nom_du_fichier_nv.csv.
Il faut passer en argument le répertoire dans lequel se trouvent les fichiers finissant par _nv.csv. Le programme essaiera d'aligner tous les fichiers finissant ainsi contenus dans ce répertoire."""

import sys
import re
import os
import urllib.request, json 
import urllib

rep=sys.argv[1]
rep=re.sub('/$', '', rep)



for fichier in os.listdir(rep):
	if re.search('_var.csv', fichier):
		varphrase={}
	
		fich=open(rep+'/'+fichier, "r")
		for ligne in fich:
			ligne=ligne.rstrip('\n')
			ligne=ligne.split('§')
			if len(ligne)!=2:
				sys.stderr.write("Erreur en traitant le fichier "+fichier+". La ligne \""+ligne+"\" n'a pas 2 cellules.\n")
			else:
				phrase=ligne[0]
				var=ligne[1]
				
				phrase=phrase.replace('"','')
				phrase=phrase.strip(' ')
				
				
				if phrase not in varphrase or varphrase[phrase]==var:
					varphrase[phrase]=var
				else:
					sys.stderr.write("Erreur en traitant le fichier "+fichier+". La phrase \""+phrase+"\" apparaît plusieurs fois avec des variétés différentes.\n")
					
		
		fichcorresp=re.sub('_var.csv', '_corresp.csv', fichier)
		
		try:
			fich=open(rep+'/exports/'+fichcorresp, "r")
		except:
			sys.stderr.write("Erreur en traitant le fichier "+fichier+". Impossible de trouver le fichier "+rep+'/exports/'+fichcorresp+".\n")
			
		
		result=""
		for ligne in fich:
			ligne=ligne.rstrip('\n')
			ligne=ligne.split('§')
			phrase=ligne[1]
			phrase=phrase.replace('"','')
			phrase=phrase.strip(' ')
			
			if phrase in varphrase:
				var=varphrase[phrase]
			else:
				var=""
				sys.stderr.write("Erreur en traitant le fichier "+fichier+". La phrase « "+phrase+" » n'apparaît pas dans le fichier d'origine.\n")
			
			result=result+"§".join(ligne)+"§"+var+'\n'
			
	
	
		
		nvfich=re.sub('_var.csv', '_corresp_var.csv', fichier)
		
		fichecr=open(rep+'/exports/'+nvfich, "w")	
		fichecr.write(result)
		fichecr.close()
		
				
