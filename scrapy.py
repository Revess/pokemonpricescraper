from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time as t

class Scraper():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.source = ""
        self.webpage = ""
        self.ebayprices = pd.DataFrame()
        self.mavin = pd.DataFrame()

    def checkIntegraty(self):
        while True:
            self.source = self.driver.page_source
            self.webpage = BeautifulSoup(self.source,features="lxml")
            if self.webpage.find("textarea",{"name":"g-recaptcha-response"}) == None:
                break
            t.sleep(1)
        return

    def renderPage(self, url):
        self.driver.get(url)
        self.source = self.driver.page_source

    def readEbayPage(self, searchOption, pokemon, id, pageNum, special):
        url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchOption}&_sacat=0&LH_Sold=1&LH_Complete=1&_ipg=200&_pgn={pageNum}'
        self.renderPage(url)
        self.webpage = BeautifulSoup(self.source,features="lxml")
        self.checkIntegraty()
        
        productslist = []
        results = self.webpage.find_all('li', {'class': 's-item'})
        for item in results:
            try:
                title = item.find('h3', {'class': 's-item__title s-item__title--has-tags'})
                if ("pokemon" in title.text.lower() or "card" in title.text.lower()) and special in title.text.lower():
                    date = item.find('div', {'class': 's-item__title--tagblock'}).find('span',{'POSITIVE'})
                    soldprice = item.find('span', {'class': 's-item__price'}).find('span')
                    link = item.find('a', {'class': 's-item__link'})

                    product = {
                        'id': id,
                        'pokemon': pokemon,
                        'title': title.text,
                        'soldprice': float(soldprice.text.replace('$','').replace(',','').strip()),
                        'date': date.text.replace("Sold","").replace(",","").replace(" ","-"),
                        'link': link['href']
                    }
                    productslist.append(product)
            except:
                print("failed")
        self.ebayprices =  pd.concat([self.ebayprices,pd.DataFrame(productslist)],ignore_index=True)
    
    def readMavin(self, searchOption, pokemon, id, pageNum, special):
        url = f'https://mavin.io/search?q={searchOption}&bt=sold&page={pageNum}'
        self.renderPage(url)
        self.webpage = BeautifulSoup(self.source,features="lxml")
        self.checkIntegraty()
        productslist = [
            {
                'id': id,
                'pokemon': pokemon,
                'title': "AVERAGE",
                'soldprice': self.webpage.find(id="worthBox").find("h4").text,
                'date': "AVERAGE",
                'link': url
            }
        ]
        results = self.webpage.find_all('div', {'class': 'row result'})
        for item in results:
            try:
                title = item.find('h4', {'class': 'item-title'})
                if ("pokemon" in title.text.lower() or "card" in title.text.lower()) and special in title.text.lower():
                    date = item.find('p', {'class': 'time'})
                    soldprice = item.find('h3', {'class': 'sold-price'})
                    link = item.find('a', {'class': 'modal-link'})
                    product = {
                        'id': id,
                        'pokemon': pokemon,
                        'title': title.text,
                        'soldprice': float(soldprice.text.replace('$','').replace(',','').strip()),
                        'date': date.text.replace("Sold","").replace(",","").replace(" ","-"),
                        'link': "https://www.mavin.io"+link['href']
                    }
                    productslist.append(product)
            except:
                print("failed")
        self.mavin =  pd.concat([self.mavin,pd.DataFrame(productslist)],ignore_index=True)
    

    def writeCSV(self,csvName):
        self.ebayprices.to_csv(csvName + ' Ebay.csv', index=False)
        self.mavin.to_csv(csvName + ' Mavin.csv', index=False)
