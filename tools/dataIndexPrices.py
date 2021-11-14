import pandas as pd
import time as t
import datetime
now = datetime.datetime.now()
# print(now.year, now.month, now.day, now.hour, now.minute, now.second)
pokemon = pd.read_csv("../data/pokemonsheet/improvedPokemonSheets.csv")
mavingPrices = pd.read_csv("../data/scrapedpricing/listings Mavin.csv")
finalDF = pd.DataFrame()

for id in range(mavingPrices["id"].max()):
    pokemonDF = mavingPrices.loc[mavingPrices["id"] == id]
    maxPrice = None
    minPrice = None
    average = None
    pokemonName = None
    #FILTERING
    pokemonDF = pokemonDF[~pokemonDF.title.str.contains("average",case=False)]
    pokemonDF = pokemonDF[~pokemonDF.title.str.contains("PSA 10",case=False)]
    if pokemon.loc[pokemon.index[id],"Rev Holo"] == 0:
        pokemonDF = pokemonDF[~pokemonDF.title.str.contains("reverse",case=False)]
    if pokemon.loc[pokemon.index[id],"Holo"] == 0:
        pokemonDF = pokemonDF[~pokemonDF.title.str.contains("holo",case=False)]
    if pokemon.loc[pokemon.index[id],"Promo"] == 0:
        pokemonDF = pokemonDF[~pokemonDF.title.str.contains("promo",case=False)]
    if not pokemonDF.empty:
        maxPrice = float(pokemonDF["soldprice"].max())
        minPrice = float(pokemonDF["soldprice"].min())
        average = 0
        for index,card in pokemonDF.iterrows():
            average += float(card["soldprice"])
        average /= pokemonDF.shape[0]
        pokemonName = pokemonDF["pokemon"].tolist()[0]
    entry = {
        "ID":id,
        "Pokemon":pokemonName,
        "mavin average":average,
        "mavin min":minPrice,
        "mavin max":maxPrice,
        "amount checked":pokemonDF.shape[0],
    }
    finalDF = finalDF.append(pd.DataFrame([entry]),ignore_index=True)

finalDF.to_csv("../data/betterpricing/mavin.csv",index=False)