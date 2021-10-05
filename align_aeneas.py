""" Ce programme aligne grâce à aenenas tous les fichiers audios et transcriptions d'un répertoire passé en argument. Attention, le programme aligne_aeneas.py doit se trouver dans la racine du répertoire aeneas. Les fichiers audios doivent être au format wav ou mp3 et avoir le même nom de fichier que leur transcription au format csv (une phrase par ligne sans autre information). """

import sys
import os
import re

repertoire=sys.argv[1]
repertoire=re.sub('/$', '', repertoire)

for fichier in os.listdir(repertoire):
	if re.search('\.(wav|mp3)$', fichier):
		nomfich=re.sub('\.(wav|mp3)$', '', fichier)
		if not os.path.isfile(repertoire+'/'+nomfich+'.csv'):
			sys.stderr.write("Pas d'équivalent en .csv trouvé pour l'audio "+fichier+". Le fichier a été ignoré.\n")
		else:
			commande=r'python3 -m aeneas.tools.execute_task '+repertoire+'/'+fichier+' '+repertoire+'/'+nomfich+'.csv "task_language=eng|os_task_file_format=json|is_text_type=plain" '+repertoire+'/'+nomfich+'.json'
   			
			sys.stderr.write('Traitement du fichier '+fichier+'...\n')
			os.system(commande) 
