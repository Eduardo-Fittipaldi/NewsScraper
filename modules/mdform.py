import markdown_strings as ms
import markdown as md
import datetime as dt
import dateparser as dp
import locale

locale.setlocale(locale.LC_TIME,"esp")

TODAY = dt.datetime.now()
DATE_FMT = " %Y-%m-%d"
MENU_FILE_NAME = TODAY.strftime("Abridged News"+ DATE_FMT)

def nlwrite(file,text = ""):
    file.write(text+"\n")

def header(text,level):
    return "#"*level + " " + text

def unorlist(text):
    return "- " + text

def link(text,link_url):
    return f"[{text}]({link_url})"

def generate_markdown(newspaper):
    
    #Creating markdown file with today's date
    filename = ".\\files\\md\\" + TODAY.strftime(newspaper.name + " %Y-%m-%d")
    file = open(filename+".md","w+",encoding="utf8")

    #Write down the header of the document
    nlwrite(file,ms.header(f"Resumen de {newspaper.name}",1))
    nlwrite(file,header(TODAY.strftime("Resumen generado el día %Y-%m-%d a las %H:%M"),4))
    
    #Add a back button to return to the HTML menu
    nlwrite(file,link(ms.bold("BACK"),"..\\" + MENU_FILE_NAME + ".html")+"  ")
    nlwrite(file,ms.horizontal_rule(3,"_"))

    for cat in newspaper.get_categories():
        
        nlwrite(file,header(ms.italics(cat),3))

        for news in newspaper.get_articles(cat):
            nlwrite(file,unorlist(link(ms.bold(news.headline),news.link)+"  "))

            if news.has_pub_day() and news.has_author():
                parsed_date = dp.parse(news.pub_day)
                final_date = parsed_date.strftime("%A %d.%m.%Y").title()
                nlwrite(file,f"{final_date} | Escrito por {news.author}")
            elif news.has_pub_day():
                parsed_date = dp.parse(news.pub_day)
                final_date = parsed_date.strftime("%A %d.%m.%Y").title()
                nlwrite(file,final_date)
            elif news.has_author():
                nlwrite(file,f"Escrito por {news.author}")
            
            nlwrite(file)

    #Save changes to markdown document.
    file.close()

def generate_html(newspaper):
    loadname = ".\\files\\md\\" + TODAY.strftime(newspaper.name + DATE_FMT)
    filename = ".\\files\\" + TODAY.strftime(newspaper.name + DATE_FMT)
    file = open(loadname +".md","r",encoding="utf8")      
    html = open(filename +".html","w")
    html.write(md.markdown(file.read(),output_format="html5",encoding="utf8"))
    html.close()

def generate_menu(newspaperlist):

    #Create .md file
    filename = ".\\files\\md\\" + MENU_FILE_NAME
    file = open(filename+".md","w+",encoding="utf8")

    #Create title
    nlwrite(file,ms.header("Noticias Resumidas - Menú",1))
    nlwrite(file,ms.horizontal_rule(3,"_"))

    #List all newspapers with corresponding files
    for newspaper in newspaperlist:
        news_path = ".\\files\\" + TODAY.strftime(newspaper.name + DATE_FMT+".html")
        nlwrite(file,header((link(ms.bold(newspaper.name),news_path)),2))
    
    #Finish editing the .md file
    file.close()
    
    #Open both the .md and .html file to finish processing into HTML
    file = open(filename+".md","r",encoding="utf8")
    html = open(MENU_FILE_NAME+".html","w+",encoding="utf8")
    html.write(md.markdown(file.read(),output_format="html5",encoding="utf8"))

    #Finish HTML processing
    html.close()

def generate_complete(newspaperlist):

    print("Generating Menu")
    generate_menu(newspaperlist)

    for newspaper in newspaperlist:
        print(f"Generating {newspaper.name}")
        generate_markdown(newspaper)
        generate_html(newspaper)