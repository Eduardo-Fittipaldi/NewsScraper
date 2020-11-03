from bs4.element import SoupStrainer
import requests
import bs4

MAX_NEWS = 8

class Newspaper:
    def __init__(self, name):
        self.name = name
        self.categories = dict()

    def add_article(self,section,article):
        self.categories.setdefault(section,[])
        self.categories[section].append(article)
    
    def get_categories(self):
        categories_list = self.categories.keys()
        return sorted(categories_list)
    
    def get_articles(self,category):
        return self.categories[category]
    
    def get_articles_number(self,category):
        if category in self.categories:
            return len(self.categories[category])
        else:
            return 0

class Article:
    def __init__(self, headline,author=None,pub_day=None,link=None):

        assert type(link) == str

        self.headline = headline
        self.author = author
        self.pub_day = pub_day
        self.link = link
    
    def has_author(self):
        return self.author != None
    
    def has_pub_day(self):
        return self.pub_day != None
    
    def has_link(self):
        return self.link != None

def get_soup(website):
    
    res = requests.get(website).text
    
    soup = bs4.BeautifulSoup(markup=res,features="html.parser")

    return soup

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def scrape_clarin():

    #Initialize the Newspaper instance for this scraper
    clarin = Newspaper("Clarín")
    
    #List of newspaper subsections, collected by hand
    subsections = {"https://www.clarin.com/politica/",
                    "https://www.clarin.com/economia/",
                    "https://www.clarin.com/sociedad/",
                    "https://www.clarin.com/mundo/"
                    }

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"section-name-sub"}).text.strip()
        articles = soup.find(attrs={"class":"box-notas"}).contents

        for box in articles:
            
            #If the amount of news reaches MAX_NEWS, stop the loop.
            if clarin.get_articles_number(section) == MAX_NEWS:
                break

            #If the current obj is not an article box, skip it.
            if type(box) is not bs4.element.Tag:
                continue
            if "des-adv" in box["class"]:
                continue
            #Retrieve the article from within the box
            article = box.article
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(["h1","h2","h3"]).text.strip()
            author = article.find(attrs={"class":"data-txt"})
            if author is not None:
                author = author.text
            
            pub_day = article.find(attrs={"class":"fecha"}).text.strip()

            link = "https://www.clarin.com" + article.a["href"]

            clarin.add_article(section,Article(headline,author,pub_day,link))
    
    return clarin

def scrape_lanacion():

    #Initialize the Newspaper instance for this scraper
    lanacion = Newspaper("La Nación")

    subsections = {"https://www.lanacion.com.ar/politica",
                "https://www.lanacion.com.ar/seguridad",
                "https://www.lanacion.com.ar/el-mundo",
                "https://www.lanacion.com.ar/salud",
                "https://www.lanacion.com.ar/educacion",
                "https://www.lanacion.com.ar/ciencia",
                "https://www.lanacion.com.ar/sociedad",
                "https://www.lanacion.com.ar/opinion"
                }

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"categoria"}).text.strip()
        articles = soup.find("section",attrs={"class":["listado"]}).contents

        for article in articles:
            
            #If the amount of news reaches MAX_NEWS, stop the loop.
            if lanacion.get_articles_number(section) == MAX_NEWS:
                break

            #If the current obj is not an article, skip it.
            if type(article) is not bs4.element.Tag:
                continue
            if article.name != "article":
                continue
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.h2.text.strip()
            if "autor" in article["class"] and article.span.a != None:
                    author = article.span.a.text
            else:
                author = None
            pub_day = article.find(attrs={"class":"fecha"}).text
            link = "https://www.lanacion.com.ar" + article.h2.a["href"]

            lanacion.add_article(section,Article(headline,author,pub_day,link))
    
    return lanacion

def scrape_ambito():
    #Initialize the Newspaper instance for this scraper
    ambito = Newspaper("Ámbito Financiero")

    subsections = {"https://www.ambito.com/contenidos/economia.html",
                    "https://www.ambito.com/contenidos/finanzas.html",
                    "https://www.ambito.com/contenidos/politica.html",
                    "https://www.ambito.com/contenidos/negocios.html"
                    }
    
    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find("h1",attrs={"class":"obj-title"}).text.strip()
        articles = soup.find_all("article",attrs={"data-type":"article"})

        for article in articles:
            
            #If the amount of news reaches MAX_NEWS, stop the loop.
            if ambito.get_articles_number(section) == MAX_NEWS:
                break
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(attrs={"class":"title"}).text.strip()
            link = article.find(attrs={"class":"title"}).a["href"]
            pub_day = soup.find("time").text

            ambito.add_article(section,Article(headline,pub_day=pub_day,link=link))
    
    return ambito

def scrape_pagina_12():
    
    #Initialize the Newspaper instance for this scraper
    pagina12 = Newspaper("Página 12")

    subsections = {"https://www.pagina12.com.ar/secciones/el-pais",
                    "https://www.pagina12.com.ar/secciones/economia",
                    "https://www.pagina12.com.ar/secciones/sociedad",
                    "https://www.pagina12.com.ar/secciones/el-mundo"
                    }

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"text-section-header"}).text.strip()
        articles = soup.find_all("article")

        for article in articles:
            
            #If the amount of news reaches MAX_NEWS, stop the loop.
            if pagina12.get_articles_number(section) == MAX_NEWS:
                break
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(attrs={"class":"title-list"}).text.strip()
            author = article.find(attrs={"class":"author"})
            if author is not None:
                author = author.a.text
            pub_day = article.find(attrs={"class":"date"}).text
            link = article.find(attrs={"class":"title-list"}).a["href"]

            pagina12.add_article(section,Article(headline,author,pub_day,link))
    
    return pagina12

def scrape_infobae():

    #Initialize the Newspaper instance for this scraper
    infobae = Newspaper("Infobae")

    subsections = {"https://www.infobae.com/politica/",
                    "https://www.infobae.com/sociedad/",
                    "https://www.infobae.com/tecno/",
                    "https://www.infobae.com/educacion/",
                    "https://www.infobae.com/campo/",
                    "https://www.infobae.com/ultimas-noticias/"
                    }

    for subsection in subsections:

        
        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"section_title"}).text.strip()
        articles = soup.find_all(attrs={"class":"card-container"})

        for article in articles:
            
            #If the amount of news reaches MAX_NEWS, stop the loop.
            if infobae.get_articles_number(section) == MAX_NEWS:
                break
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.find(attrs={"class":"headline"}).h2.text.strip()
            link = article.find(attrs={"class":"headline"}).a["href"]
            link = "https://www.infobae.com" + link

            infobae.add_article(section,Article(headline,link=link))
    
    return infobae

def scrape_perfil():
       
    #Initialize the Newspaper instance for this scraper
    perfil = Newspaper("Diario Perfil")

    subsections = {"https://www.perfil.com/seccion/politica/",
                    "https://www.perfil.com/seccion/economia/",
                    "https://www.perfil.com/seccion/sociedad/",
                    "https://www.perfil.com/seccion/internacional",
                    "https://www.perfil.com/ultimo-momento/"}

    for subsection in subsections:

        soup = get_soup(subsection)
        section = soup.find(attrs={"class":"tituloCanal"}).text.strip()
        articles = soup.find_all("article")

        for article in articles:
            
            #If the amount of news reaches MAX_NEWS, stop the loop.
            if perfil.get_articles_number(section) == MAX_NEWS:
                break
            if "bannerEntreNotas" in article["class"]:
                continue
            
            #Scrape the main data (headline, author, link, publication date)
            headline = article.h2.a.text.strip()
            pub_day = article.find(attrs={"class":"dateTime"})
            if pub_day is not None:
                pub_day = pub_day.text.strip()
            link = remove_prefix(article.a["href"],"https://www.perfil.com")
            link = "https://www.perfil.com" + link
            perfil.add_article(section,Article(headline,pub_day=pub_day,link=link))
    
    return perfil

def scrape_everything():
    newspapers = list()
    newspapers.append(scrape_ambito())
    newspapers.append(scrape_clarin())
    newspapers.append(scrape_infobae())
    newspapers.append(scrape_lanacion())
    newspapers.append(scrape_pagina_12())
    newspapers.append(scrape_perfil())
    return newspapers