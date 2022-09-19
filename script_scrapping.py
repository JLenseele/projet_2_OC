import requests
from bs4 import BeautifulSoup, SoupStrainer
import csv

#def is_long_string(string):
#   return len(string) > 200
def ecriture(nom_fichier, url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url ):

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
	
	data = [url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url]
	
	with open(nom_fichier, 'w') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(en_tete)
		# zip permet d'itérer sur deux listes à la fois
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
	

def etl():
	#page à recuperer
	url = "http://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
	reponse = requests.get(url)
	page = reponse.content

	#parse de la page en soup
	soup = BeautifulSoup(page, "html.parser")

	#recuperation des données
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

	i=0

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
	
	#verif itération
	'''
	print(dir(url)
	print(dir(upc)
	print(dir(titre)
	print(dir(price_incl)
	print(dir(price_excl)
	print(dir(number_available)
	print(dir(description)
	print(dir(categorie)
	print(dir(review_rating)
	print(dir(image_url)
	'''
	#verification des données
	'''
	print(url)
	print(upc)
	print(titre)
	print(price_incl)
	print(price_excl)
	print(number_available)
	print(description)
	print(categorie)
	print(review_rating)
	print(image_url)
	'''
	ecriture('data.csv', url, upc, titre, price_incl, price_excl, number_available, description, categorie, review_rating, image_url)
#	paragraphe = SoupStrainer("p")
#	only_long_string = SoupStrainer(string=is_long_string)
#	print(BeautifulSoup(page, "html.parser", parse_only=only_long_string).prettify())

etl()
