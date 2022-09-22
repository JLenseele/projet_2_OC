<a name="readme-top"></a>
# Book To Scrap

Scrapping du site [Book To Scrap](http://books.toscrape.com/) vers du fichier.csv

## Features

Récupère l'ensemble des données du site [Book To Scrap](http://books.toscrape.com/) dans un fichier .csv par catégorie de livre.

## Requirements

+ [Python v3+](https://www.python.org/downloads/)

## Installation & Get Started

Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/projet_2_OC.git
    cd projet_2_OC

Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    
Lancer le Script

    python script_scrapping.py

## Usage

Aprés lancement, le script commence à scrapper et enregistrer les données de chaque produit dans le dossier data (dossier qui sera créé),  
dans un fichier au format suivant : data_nom_de_catégorie.csv  

Afin d'utiliser les données éditées, il convient d'importer ces fichiers dans un tableur (ex [Google Sheets](https://docs.google.com/spreadsheets))  

**Utiliser le délimiteur ","**  

![image](https://user-images.githubusercontent.com/113677278/191808350-58f83375-84f3-4d9a-910c-88f110115a11.png)


Il récupère également l'image de chaque produit dans le dossier img

## Roadmap

- [x] Scrapp page produit
- [x] Scrapp Catégorie de produit
- [x] Scrapp Site complet
- [x] Récupération des images de chaque produit
- [ ] Interface Graphique avcec choix de recherche
    - [ ] Scrapping d'un livre
    - [ ] Scrapping d'une catégorie spécifique
    - [ ] Scrapping du site complet

<p align="right">(<a href="#readme-top">back to top</a>)</p>
    
## Reference

+ [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
+ [Requests](https://pypi.org/project/requests/)  

## Contributors

[JLenseele](https://github.com/JLenseele)
