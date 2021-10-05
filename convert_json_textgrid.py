""" Ce programme convertit tous les fichier json d'un répertoire passé en argument en fichiers TextGrid pour Praat. Les fichiers json doivent être des fichiers de sortie de l'aligneur aeneas. """

import sys
import os
import re
import json


repertoire=sys.argv[1]
repertoire=re.sub('/$', '', repertoire)

for fichier in os.listdir(repertoire):
	if re.search('\.json$', fichier):
		with open(repertoire+'/'+fichier) as json_file:
    			data = json.load(json_file)
    			sys.stderr.write('Traitement du fichier '+fichier+'...\n')
    			
    			content='File type = "ooTextFile"\nObject class = "TextGrid"\n\nxmin = 0\nxmax = ?\ntiers? <exists>\nsize = 1\nitem []:\n    item [1]:\n        class = "IntervalTier"\n        name = "transcription"\n        xmin = 0\n        xmax = ?\n        intervals: size = ?'
    			
    			fragments=data['fragments']
    			cpt=0
    			for phrase in fragments:
    				cpt+=1
    				debut=phrase['begin']
    				fin=phrase['end']
    				texte=phrase['lines']
    				texte=' '.join(texte)
    				
    				content=content+'\n        intervals ['+str(cpt)+']:\n            xmin = '+debut+'000\n            xmax = '+fin+'\n            text = "'+texte+'"'
    				
    				
    			
    			
    			content=content.replace('xmax = ?', 'xmax = '+fin)
    			content=content.replace('intervals: size = ?', 'intervals: size = '+str(cpt))
    			
    			nomfich=re.sub('\.json$', '', fichier)
    			textgrid=open(repertoire+'/'+nomfich+'.TextGrid', 'w')
    			textgrid.write(content)
    			textgrid.close()
 
    	
