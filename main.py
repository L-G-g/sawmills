from bs4 import BeautifulSoup
import numpy as np
import requests
import csv

def get_usa_pages():

    usa_sawmills = "https://www.sawmilldatabase.com/country_sawmills.php?id=11"

    response = requests.get(usa_sawmills).text
    soup = BeautifulSoup(response, features="lxml")
    tbody = soup.find_all('td')
    usa_list = []
    active = 0

    for td in tbody:
        if 'Closed or Sold Sawmills' in str(td):
            break
        if 'Active Sawmills' in str(td):
            active = 1
            pass
        if active == 1:
            try:
                usa_list.append(td.find('a').get('href'))
            except AttributeError:
                pass
    
    all_pages = []
    
    for Sawmill in usa_list:
        pag='https://www.sawmilldatabase.com/' + str(Sawmill)
        all_pages.append(pag)

    return all_pages

def get_final_url(url):

    def has_website():
        if td_objects is not None:
            str_objects = [str(a) for a in td_objects]
            if "Website" in str_objects[0]:
                return True
    
    final_url = "no data"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    td_objects = soup.find("td")

    if has_website():
        final_url = "check"
        objects = soup.find_all("a")
        href_objects = [a.get('href') for a in objects]

        for line in href_objects:
            try:
                if line.startswith('http://'):
                    final_url = line
            except AttributeError:
                pass
    
    name = soup.select('h1')[0].text.strip()
    return name, final_url

def run_all():
    all_pages = get_usa_pages()
    print(all_pages)
    list_of_tup = []

    for page in all_pages:
        list_of_tup.append(get_final_url(page))

    return list_of_tup

if __name__ == '__main__':

    list_of_tup = run_all()

    with open('usa_sawmills.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f , lineterminator='\n')
        for tup in list_of_tup:
                writer.writerow(tup)