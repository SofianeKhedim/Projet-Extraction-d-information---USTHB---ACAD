
import sys,re,urllib,requests
from bs4 import BeautifulSoup as bs



# Fonctions
def verifier_intervalle(interval):
	global debut,fin
	if re.match('[A-Z]-[A-Z]',interval) and interval[0]<=interval[2]:
		debut = interval[0]
		fin = interval[2] 
	else:
		print('Intervalle invalide ❌\n')
		exit()

def verifier_port(port):
	if 0 <= int(port) <= 1023:
		print('Port valide ✅\n')
	else:
		print('Port invalide ❌\n')
		exit()

	return port

def bs4_to_string(data):
	return [str(item) for item in data]

# Constantes
DOSSIER_VIDAL = 'vidal/vidal-Sommaires-Substances-'
FICHIER_INFO = 'infos1.txt'
FICHIER_DIC = 'subst.dic'


if len(sys.argv) > 2: # Configuration en fonction des arguments du script
	verifier_intervalle(sys.argv[1].upper())
	port = verifier_port(sys.argv[2])
elif len(sys.argv) == 2:
	verifier_intervalle(sys.argv[1].upper())
	port ='80'
else: # Configuration par défaut
	debut = 'A'
	fin = 'Z'
	port= '80'



url_base = f'http://localhost:{port}/{DOSSIER_VIDAL}'
info = open(FICHIER_INFO,'w')

medicaments = []
nbr_total  = 0

while debut <= fin:
	url = f'{url_base}{debut}.html'
	resultat = requests.get(url)
	
	if resultat.status_code == 200:
		# Extraction des données HTML
		html = bs(resultat.text.encode('latin1').decode(),'html.parser') # Corriger les chars spéciaux
		data = html.find_all('li')
		data = bs4_to_string(data) # Convertir les éléments BS en String

		nbr = 0
		for i in data: #Filtrer data pour ne laisser que les substances.
			if '<a href=\"Substance/' in i:
				# Extraction des noms de substances
				med = re.findall('.htm">(.+)</a>',i)
				medicaments.append(med[0])
				nbr += 1
			else:
				data.remove(i) # Non substance

		nbr_total  += nbr
		# info.write(f"Le nombre de medicament commencant par la lettre  {debut} = {nbr}\n") # Sauvegarder le nombre d'entités cet lettre
		info.write(f"Total de {debut} = {nbr}\n") # Sauvegarder le nombre d'entités cet lettre

		print(f'\nURL = "{url}" : Processus terminé avec succès ✅\n')
	else:
		print(f'\nÉchec de la requête pour l\'URL : "{url}"\n')

	
	debut = chr(ord(debut)+1) 

info.write("------------------------------------------\n")
info.write(f"Nombre total des substances actives = {nbr_total}") 
print('infos1.txt est généré avec succès.')
info.close()

substances = '\n'.join([f"{item},.N+subst" for item in medicaments]) # Convertir la Liste en une seule String pour l'écrire dans 'subst.dic'
open(FICHIER_DIC,'w',encoding='utf-16le').write('\ufeff' + substances)

print(f'{FICHIER_DIC} est créé avec succès.')
