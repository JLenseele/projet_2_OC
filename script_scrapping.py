import os.path

import requests
from bs4 import BeautifulSoup
import csv
#enregistrement d'image
import urllib.request
#re.sub titre image
import re

def parse(url):
	reponse = requests.get(url)
	page = reponse.content
	soup = BeautifulSoup(page, "html.parser")
	return soup

def ecriture(datas, nom_fichier_section):

# definition de l'en-tete pour le fichier final
	en_tete = ['product_page_url'
				,'universal_product_code (upc)'
				,'title'
				,'price_including_tax'
				,'price_excluding_tax'
				,'number_available'
				,'product_description'
				,'category'
				,'review_rating'
				,'image_url']

#creation du dossier data s'il n'existe pas
	file_path_data = "./data/"
	if not os.path.exists(file_path_data):
		os.makedirs(file_path_data)

# ecriture dans un fichier avec le nom de la section en cour + encoder en utf-8 pour eviter les erreurs de 'charmap'
	with open(file_path_data + nom_fichier_section, 'w', encoding="utf-8") as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(en_tete)
		for data in datas:
			writer.writerow(data)
	pass
def listing_url_page_produit(url_section):

	url_section_liste = []
	links_produit = []
# on ajoute par defaut la premiere page de la section "index.html"
	url_section_liste.append(url_section)
	soup = parse(url_section)	
# vérification de l'existence d'autre page de la même section
	other_pages = soup.find('li', class_="current")
	if not other_pages:
		pass
	else:
# on determine combien il y a de page
		other_page = other_pages.text.strip()
		nombre_page = other_page[len(other_page)-1:]
		i = int(nombre_page)
		while i > 1:
# on ajoute les différentes page dans une liste
			url_section_liste.append(url_section.replace('index', 'page-' + str(i)))
			i = i - 1

	for x in url_section_liste:
		soup = parse(x)
# on va recuperer tout les h3 qui contiennent les url des pages produit
		url_produits = soup.find_all('h3')	
		i = 0
# dans chaque element trouvé, on recupere l'url href dans la balise <a>
		for url_produit in url_produits:
			url_produit = url_produits[i].a
			links_produit.append("http://books.toscrape.com/catalogue/" + url_produit.get('href').replace('../', ''))
			i = i + 1
	
	return links_produit

def recup_data_produit(url):

	soup = parse(url)
	
# vérification multiple pour recupérer les données demandées
	i=0
	excract = soup.find_all("tr")
	for x in excract:
		x = excract[i].th.string
		y = excract[i].td.string
		if x == "UPC":
			upc = y
		elif x == "Price (excl. tax)":
			price_excl = y
		elif x == "Price (incl. tax)":
			price_incl = y
		elif x == "Availability":
			number_available = y
		else:
			none=y
		i=i+1

# utilisation de la function rate pour recupérer la note
		# on cherche uniquement la div qui inclut la note
	div_rating = soup.find_all('div', class_='col-sm-6 product_main')
# puis la liste des <P> de cette div
	p_rating = div_rating[0].find_all('p')
# on cherche la classe qui indique la note
	i = 0
	star = [['star-rating', 'Five'], ['star-rating', 'Four'], ['star-rating', 'Three'], ['star-rating', 'Two'],
			['star-rating', 'One']]
	note = ['5', '4', '3', '2', '1']
	while i < len(p_rating):
		tag = p_rating[i]
		if tag['class'] == star[0]:
			rating = note[0]
			i = len(p_rating)
		elif tag['class'] == star[1]:
			rating = note[1]
			i = len(p_rating)
		elif tag['class'] == star[2]:
			rating = note[2]
			i = len(p_rating)
		elif tag['class'] == star[3]:
			rating = note[3]
			i = len(p_rating)
		elif tag['class'] == star[4]:
			rating = note[4]
			i = len(p_rating)
		else:
			rating = "pas de note"
		i = i + 1
		pass
# recuperation du premier H1 qui correspond au titre
	titre = soup.select('h1')[0].text
# recuperation de la description
	description = soup.select('p')[3].text
# récupération de la categorie en 4eme lien
	categorie = soup.select('a')[3].text
# recupération de l'url de l'image si src = titre
	image_urls = soup.find_all('img', alt=titre)
	links = []
	for image_url in image_urls:
		links.append("http://books.toscrape.com/" + image_url['src'].replace('../', ''))
	image_url = links[0]

#enregistrement de l'image dans un dossier "img" que l'on créer s'il n'existe pas
	file_path_img = "./img/"
	if not os.path.exists(file_path_img):
		os.makedirs(file_path_img)
# suppression des caracteres speciaux dans les titres d'images
	titre_propre = re.sub('[^a-zA-Z0-9\n\. ]', '', titre)
# enregistrement des images de page produit dans le dossier img
	urllib.request.urlretrieve(image_url, "./img/" + titre_propre + ".jpg")

# ajout des données récupérées dans DATA pour ensuite l'écrire dans un fichier
	data = [url, upc, titre, price_incl, price_excl, number_available, description, categorie, rating, image_url]

	return data
def etl():

# page à recuperer
	soup = parse("http://books.toscrape.com/index.html")

# on vérifie et recupere les URLs et les titres d'une section
	url_sections = []
	i = 0
	for url_section in soup.find_all('a'):
		if 'catalogue/category/books/' in url_section.get('href'):
			url_sections.append(url_section.get('href'))
			titre_section = url_section.get_text()

# puis les URLs des produit
			url_produits = listing_url_page_produit("http://books.toscrape.com/" + url_sections[i])
			datas = []

# on recupere les donnees de tout les produits
			for url_produit in url_produits:
				datas.append(recup_data_produit(url_produit))

# enfin on enregistre les datas dans un csv au nom de la section
			ecriture(datas, 'data_'+ titre_section.strip() +'.csv')
			print('la catégorie "' + titre_section.strip() + '" est maintenant enregistrée.')
			i = i +1
		else:
			pass
etl()