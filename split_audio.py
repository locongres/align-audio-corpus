""" Ce fichier découpe des fichiers audios phrase à phrase à partir d'un fichier TextGrid. Il prend en argument le répertoire des fichiers. Pour chaque fichier nom_du_fichier.TextGrid, il recherche un fichier nom_du_fichier.wav et crée dans un sous-dossier "exports" un fichier wav par phrase. Il crée aussi un fichier nom_du_fichier_corresp.csv sous la forme fichier_son§phrase_transcrite indiquant la correspondance entre les fichiers créés et leur transcription.
Il faut passer en argument le répertoire dans lequel se trouvent les fichiers à découper. Le programme essaiera de découper tous les fichiers wav contenus dans ce répertoire."""


import sys
import re
from pydub import AudioSegment
import textgrids
import os



entree=sys.argv[1]
entree=re.sub('/$', '', entree)
		
try:
	os.mkdir(entree+"/exports")
except:
	sys.stderr.write('Le répertoire "'+entree+'/exports" n\'a pas pu être créé.\n')

for nomfich in os.listdir(entree):
	if re.search('\.wav$', nomfich):
		fichtier=re.sub('\.wav$', '.TextGrid', nomfich) 
		
		if not os.path.exists(entree+"/"+fichtier):
			sys.stderr.write('Le fichier "'+fichtier+'" n\'existe pas".\n')
		else:
		
			nomfichorig=re.sub('\.wav$', '', nomfich)
			try:
				grid = textgrids.TextGrid(entree+"/"+fichtier)
			except:
				sys.stderr.write('Le fichier "'+fichtier+'" n\'a pas pu être lu.\n')



			if 'transcription' not in grid:
				sys.stderr.write('Le fichier "'+fichtier+'" ne comporte pas de tiere appelée "transcription".\n')
			else:
				intervals=grid['transcription']
				
				cptfich=0
				transcrfich=[]
				
				for interval in intervals:
					xmax=interval.xmax
					xmin=interval.xmin
					text=interval.text
					
					if text!="":
						cptfich+=1

						newAudio = AudioSegment.from_wav(entree+"/"+nomfich)
						
						deb = xmin * 1000
						fin= xmax * 1000
						deb=deb-30
						if deb<0:
							deb=0
						fin=fin+50
						if fin>len(newAudio):
							fin=len(newAudio)
							
						newAudio = newAudio[deb:fin]
						newAudio.export(entree+'/exports/'+nomfichorig+'_'+str(cptfich)+".wav", format="wav")
						
						transcrfich.append((nomfichorig+'_'+str(cptfich)+".wav", text))


				monfichier=open(entree+'/exports/'+nomfichorig+'_corresp.csv', 'w')
				monfichier.close()

				for item in transcrfich:
					monfichier=open(entree+'/exports/'+nomfichorig+'_corresp.csv', 'a')
					monfichier.write(item[0]+'§'+item[1]+'\n')
					monfichier.close()
	



