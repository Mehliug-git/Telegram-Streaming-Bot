"""
UTILE POUR TESTER LES SITES UN PAR UN
TODO :
https://wwvv.cpasmieux.one/ 

:)
"""

from bs4 import BeautifulSoup
import requests
import re   

URL = ["https://cpasmieux.cc/"]
film = "Rick morty"#remplacer par le user imput de telegram
search_lower = film.lower()


search = search_lower.replace(' ', '+')#POST Payload convert
str_search = str(search)
data = {"do":"search", "subaction":"search", "story": {search}}
headers= {
        "Content-Type": "application/x-www-form-urlencoded",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
}

result = search_lower.split()#fait une liste avec le nom du film si plusieurs mots pour chercher dans les URL


for i in URL:
    page = requests.get(i, data=data, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser').find_all(lambda t: t.name == "a")
    url_list = [a["href"] for a in soup]#https://stackoverflow.com/questions/65168254/how-to-get-href-link-by-text-in-python
    for __ in result:
        msg = list(filter(lambda x: re.search(__, x), url_list))

    print(f'LA PTN DE LIST DURL DE SES MORTS :\n\n\n {page.text}')
print(page)


