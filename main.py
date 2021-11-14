from scrapy import Scraper
import pandas as pd
import time as t

scraper = Scraper()
indexedCards = pd.read_csv("./data/pokemonsheet/1999formatted.csv")

for index, card in indexedCards.iterrows():
    special = "pokemon"
    searchOptions = f'{card["Card"]}+{card["Year"]}+{card["Code"]}'
    if "Energy" in card["Card"] or "Energie" in card["Card"]:
        searchOptions += "+"+card["Type"]
    if card["Holo"] == "1":
        searchOptions += "+Holo"
        special = "promo"
    if card["Rev Holo"] == "1":
        searchOptions += "+Reverse Holo"
        special = "promo"
    if card["Promo"] == "1":
        searchOptions += "+Promo"
        special = "promo"
    if card["Country"] == "NL":
        searchOptions += "+NL"
    for i in range(1,2):
        scraper.readEbayPage(searchOptions,card["Card"],index,i,special=special)
        scraper.readMavin(searchOptions,card["Card"],index,i,special=special)
    t.sleep(1)

scraper.writeCSV("listings")