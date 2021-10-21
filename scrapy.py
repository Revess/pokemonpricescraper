from bs4 import BeautifulSoup
import pandas as pd
from csv import reader
from selenium import webdriver
import time as t


items = []
prices = []
pokemon = "pikachu"
year = "1999"
cardIndex = "60%2F64"
num_pages = 10

def getSearches(csvfile):
    searches = []
    with open(csvfile, 'r') as f:
        csv_reader = reader(f)
        for row in csv_reader:
            searches.append(row[0])
    return searches

def renderPage(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    t.sleep(5)
    r = driver.page_source
    return r

def getData(pokemon, year, cardIndex,pageNum):
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={pokemon} {year} {cardIndex}&_sacat=0&LH_Sold=1&LH_Complete=1&_pgn={pageNum}'
    r = renderPage(url)
    soup = BeautifulSoup(r,features="lxml")
    print(soup.prettify())
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('li', {'class': 's-item'})
    for item in results:
        print(item)
        title = item.find('h3', {'class': 's-item__title s-item__title--has-tags'})
        soldprice = item.find('span', {'class': 's-item__price'}).find('span').value
        bids = item.find('span', {'class': 's-item__bids'})
        link = item.find('a', {'class': 's-item__link'})
        print(type(title),type(soldprice),type(bids),type(link))
        product = {
            'title': title.text,
            'soldprice': float(soldprice.text.replace('$','').replace(',','').strip()),
            'bids': bids.text,
            'link': link['href'],
        }
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    print(productsdf)
    exit()
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = getData(pokemon,year,cardIndex,1)
productslist = parse(soup)
output(productslist, pokemon)