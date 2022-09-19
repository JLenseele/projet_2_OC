import requests
from bs4 import BeautifulSoup, SoupStrainer
import csv

#def is_long_string(string):
#   return len(string) > 200
def ecriture(datas, nom_fichier):

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
	
	with open(nom_fichier, 'w', encoding="utf-8") as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(en_tete)
		for data in datas:
			writer.writerow(data)

	pass
	
def rate(soup):
	
	# on cherche uniquement la div qui inclut la note
	div_rating = soup.find_all('div', class_='col-sm-6 product_main')
	
	# puis la liste des <P> de cette div
	p_rating = div_rating[0].find_all('p')

	#on cherche la classe qui indique la note
	i=0
	star = [['star-rating', 'Five'],['star-rating Four'],['star-rating Three'],['star-rating Two'],['star-rating One']]
	note = ['5','4','3','2','1']
	while i < len(p_rating):
		tag = p_rating[i]
		if tag['class'] == star[0]:
			rating = note[0]
			i = len	(p_rating)
		elif tag['class'] == star[1]:
			rating = note[1]
			i = len	(p_rating)
		elif tag['class'] == star[2]:
			rating = note[2]
			i = len	(p_rating)
		elif tag['class'] == star[3]:
			rating = note[3]
			i = len	(p_rating)
		elif tag['class'] == star[4]:
			rating = note[4]
			i = len	(p_rating)
		else:
			rating = "pas de note"
		
		i = i + 1
		pass

	return rating

def listing_url_page_produit(url_section):

	url_section_liste = []
	links_produit = []
	url_section_liste.append(url_section)

	reponse = requests.get(url_section)
	page_produit = reponse.content
	soup = BeautifulSoup(page_produit, 'html.parser')
	
	# vérification de l'existence d'autre page de la même section
	other_pages = soup.find('li', class_="current")
	if not other_pages:
		pass
	else:
		#on determine combien il y a de page
		other_page = other_pages.text.strip()
		nombre_page = other_page[len(other_page)-1:]
		i = int(nombre_page)
		while i > 1:
			# on ajoute les différentes page dans une liste
			url_section_liste.append(url_section.replace('index', 'page-' + str(i)))
			i = i - 1

	for x in url_section_liste:
		reponse = requests.get(x)
		page_produit = reponse.content
		soup = BeautifulSoup(page_produit, 'html.parser')
		#on va recuperer tout les h3 qui contiennent les url des pages produit
		url_produits = soup.find_all('h3')	
		i = 0
		#dans chaque element trouvé, on recupere l'url href dans la balise <a>
		for url_produit in url_produits:
			url_produit = url_produits[i].a
			links_produit.append("http://books.toscrape.com/catalogue/" + url_produit.get('href').replace('../', ''))
			i = i + 1
	
	return links_produit

def recup_data_produit(url):

	reponse = requests.get(url)
	page = reponse.content

	#parse de la page en soup
	soup = BeautifulSoup(page, "html.parser")
	
	#vérification multiple pour recupérer les données demandées
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
	review_rating = rate(soup)
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
	
	data = [url, upc, titre, price_incl, price_excl, number_available, description, categorie, review_rating, image_url]
	
	return data

def etl():
	#page à recuperer
	url_site = "http://books.toscrape.com/index.html"

	url_sections = "http://books.toscrape.com/catalogue/category/books/classics_6/index.html"
	url_produits = listing_url_page_produit(url_sections)

	datas = []
	for url_produit in url_produits:
		datas.append(recup_data_produit(url_produit))
	
	#fonction ecriture pour enregistrer les datas dans un csv
	ecriture(datas, 'data.csv')
	

etl()
