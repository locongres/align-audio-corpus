# -*-coding:Utf-8 -*
""" Divise en phrase et met dans des fichiers csv en sortie le contenu de fichiers txt d'un répertoire passé en entrée. """


import re
import sys
import os
	

ponctuations='\.\?\!;;:,…\[\]\(\)\{\}"«»/\\^_`\*”“„‘´\$\#\%‰\&\+<>=\`\|\~\*\ë£ƒ¥€¿¡¢¥─—¯¤¯´±°¹²³™¶'
ponctuationsweb='\.\?\!;;:,…\[\]\(\)\{\}"«»\\^_`\*”“„‘´\$\#\%‰\&\+<>=\`\|\~\*\ë£ƒ¥€¿¡¢¥─—¯¤¯´±°¹²³™¶'

pasciv='([^A-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÇers ]|[^mlM]e|[^M]me|[^l]le|[^M]lle|[^ M]M|[^ ]MM|[^DPg]r|[^M]gr]|[^er]s|[^lmM]es|[^PDg]rs|[^l]les|[^M]lles]|[^M]mes|[^M]grs]|[^MJ ][A-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÇ]|[^ ][MJ][A-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÇ])'


motifs=[
	#mails
	('([^'+ponctuationsweb+'\s×]*?)([\.]?)([^'+ponctuationsweb+'\s×]*?)@([^'+ponctuationsweb+'\s×]*?)\.([^'+ponctuationsweb+'\s×]*?)',5),
	#sites
	('https?://(([^'+ponctuationsweb+'\s×]|[/\.])+)((\.[a-z]+)?)',2),
	('www\.(([^'+ponctuationsweb+'\s×]|[/\.])+)',2),
	('(([^'+ponctuationsweb+'\s×]|[/\.])+)\.(org|com|fr|net|eu|it|bzh|cat|tv)((/([^'+ponctuationsweb+'\s×]|[/\.])*?)?)',6),
	#téléphones
	('\+([0-9]+)(\(0\))?([0-9 ]+)',3),
	('0([0-9]{5,})',1),
	('0([0-9])( [0-9]{2})+',2),
	#dates
	('([0-9]{1,2})(\/|\-|\.)([0-9]{1,2})(\/|\-|\.)([0-9]{4})', 5),
	('([0-2])?([0-9])(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([0-9]{2})', 7),
	('([0-2])?([0-9])(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([0-9]{2})', 7),
	('([3])?([0-1])(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([0-9]{2})', 7),
	('([3])?([0-1])(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([0-9]{2})', 7),
	('([0-9]{4})(\/)([0-9]{1,2})(\/|\-|\.)([0-9]{1,2})', 5),
	('([0-9]{2})(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([0-2])?([0-9])', 7),
	('([0-9]{2})(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([0-2])?([0-9])', 7),
	('([0-9]{2})(\/|\-|\.)([0])?([1-9])(\/|\-|\.)([3])?([0-1])', 7),
	('([0-9]{2})(\/|\-|\.)([1])?([0-2])(\/|\-|\.)([3])?([0-1])', 7),
	('([0-2])?([0-9])(\/)([0])?([1-9])', 5),
	('([0-2])?([0-9])(\/)([1])?([0-2])', 5),
	('([3])?([0-1])(\/)([0])?([1-9])', 5),
	('([3])?([0-1])(\/)([1])?([0-2])', 5),
	('([0])([1-9])(\/|\-)([0-9]{4})', 4),
	('([1])([0-2])(\/|\-)([0-9]{4})', 4),
	('([0])([1-9])(\/)([4-9])([0-9])', 5),
	('([1])([0-2])(\/)([4-9])([0-9])', 5),
	('([0])([1-9])(\/)([3])([2-9])', 5),
	('([1])([0-2])(\/)([3])([2-9])', 5),
]


def split_sentences(texte):
	""" Divise un texte en phrases. Retourne une liste de phrases.
	:param texte: texte à diviser """

	#Nettoyage
	texte=texte.replace('§', '')
	texte=re.sub('<br ?/? ?>', '§', texte)
	texte=re.sub('\\n', '§', texte)

	#Point suivi d'une majuscule (sauf si précédé d'une civilité ou une initiale)
	texte=re.sub(pasciv+'([\.\?\!…]) ([A-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÇÆŒ"”“«»])', '\g<1>\g<2>§\g<3>', texte)

	#Autres points suivis d'une majuscule 
	texte=re.sub('([\?\!…]) ([A-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÇÆŒ"”“«»])', '\g<1>§\g<2>', texte)
	
	#Point (sauf normal et suspension) pas suivi de guillement
	texte=re.sub('([\?\!])', '\g<1>§', texte)
	
	#Trois points sans espace
	texte=re.sub('([…])([A-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÇÆŒ])', '\g<1>§\g<2>', texte)
	
	#Après deux points guillemets
	texte=re.sub(': ?([«"”“])', ':§\g<1>', texte)
	
	#Guillemet suivant une ponctuation
	texte=re.sub('([\.\?\!…])( ?)([»"”“])', '\g<1>\g<2>\g<3>§', texte)
	
	#Guillemets d'affilée
	texte=re.sub('» ?«', '»§«', texte)
	texte=re.sub('(["”“]) ?(["”“])', '\g<1>§\g<2>', texte)
	
	
	#Si la phrase commence par un guillemet mais qu'il n'y en a pas de fin, on isole le guillemet
	texte=re.sub('(^|§) ?([«])([^»§]*?)(§|$)', '\g<1>§\g<2>§\g<3>\g<4>', texte)
	texte=re.sub('(^|§) ?(["”“])([^"”“§]*?)(§|$)', '\g<1>§\g<2>§\g<3>\g<4>', texte)
	
	#Si la phrase finit par un guillemet mais qu'il n'y en a pas de début, on isole le guillemet
	texte=re.sub('(^|§)([^«§]*?)([»]) ?(§|$)', '\g<1>\g<2>§\g<3>§\g<4>', texte)
	texte=re.sub('(^|§)([^"”“§]*?)(["”“]) ?(§|$)', '\g<1>\g<2>§\g<3>§\g<4>', texte)
	
	#Si la phrase commence et finit par un guillemet, sans guillement entre, on isole les guillemets
	texte=re.sub('(^|§) ?([«])([^«»§]*?)([»]) ?(§|$)', '\g<1>§\g<2>§\g<3>§\g<4>', texte)
	texte=re.sub('(^|§) ?(["”“])([^"”“§]*?)(["”“]) ?(§|$)', '\g<1>§\g<2>§\g<3>§\g<4>', texte)
	
	#S'il y a un guillemet ouvrant mais pas de fermant avant la fin
	texte=re.sub('([«])([^»§]*?)(§|$)', '§\g<1>§\g<2>\g<3>', texte)
	
	#S'il y a un guillemet fermant mais pas d'ouvrant avant la fin
	texte=re.sub('(^|§)([^«§]*?)([»])', '\g<1>\g<2>§\g<3>§', texte)
	
	#On nettoie
	texte=re.sub('(§{1,})', '§', texte)
	
	#Si la phrase commence par un guillement de fin, on l'isole
	texte=re.sub('(^) ?([»])', '\g<1>§\g<2>§', texte)
	texte=re.sub('(§{1,})', '§', texte)
	
	#S'il y a des guillemets ou des ponctuations tous seuls, on les colle à la phrase d'avant out d'après
	texte=re.sub('(^|§)( ?)«( ?)§', '\g<1>\g<2>«\g<3>', texte)
	texte=re.sub('(^|§)( ?)“( ?)§', '\g<1>\g<2>«\g<3>', texte)
	texte=re.sub('^( ?)(["”“])( ?)§', '\g<1>\g<2>\g<3>', texte)

	while re.search('§( ?)([^0-9a-záàâäèéëêíìïîòóôöùúüûñçæœA-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÑÇÆŒ]+)( ?)(§|$)', texte) or re.search('§( ?)([^0-9a-záàâäèéëêíìïîòóôöùúüûñçæœA-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÑÇÆŒ«"”“]+) ', texte):
		texte=re.sub('§( ?)([^0-9a-záàâäèéëêíìïîòóôöùúüûñçæœA-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÑÇÆŒ]+)( ?)(§|$)', '\g<1>\g<2>\g<3>\g<4>', texte)
		texte=re.sub('§( ?)([^0-9a-záàâäèéëêíìïîòóôöùúüûñçæœA-ZÁÀÂÄÈÉÊËÌÍÎÏÒÓÔÖÙÚÛÜÑÇÆŒ«"”“]+) ', '\g<1>\g<2>§', texte)

	
	#On nettoie
	texte=re.sub('§([ ]{1,})', '§', texte)
	texte=re.sub('([ ]{1,})§', '§', texte)
	texte=re.sub('([§]{2,})', '§', texte)
	texte=texte.strip(' ')
	texte=texte.strip('§')
	
	
	phrases=texte.split('§')
	
	return phrases
	

repertoire=sys.argv[1]
repertoire=re.sub('/$', '', repertoire)

for nomfich in os.listdir(repertoire):
	if re.search('\.txt$', nomfich):
		fichier=open(repertoire+'/'+nomfich, 'r')
		nvnom=re.sub('\.txt$', '', nomfich)

		content=fichier.read()
		phrases=split_sentences(content)
		
		nvfich=open(repertoire+'/'+nvnom+'.csv', 'w')
		nvfich.close()

		for phrase in phrases:
			nvfich=open(repertoire+'/'+nvnom+'.csv', 'a')
			nvfich.write(phrase+'\n')
			nvfich.close()

