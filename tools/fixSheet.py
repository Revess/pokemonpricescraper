import pandas as pd
import time as t

indexedCards = pd.read_csv("../data/pokemonsheet/1999.csv").drop(["File Name", "Troll&Toad Price", "Subtotal"], axis=1)
passedValues = pd.DataFrame(columns=list(indexedCards.columns))

indexedCards[['CardNr','Set']] = indexedCards['Code'].str.split('/',expand=True)

for index, card in indexedCards.iterrows():
    if not card["Card"] in passedValues["Card"].tolist():
        card["CardNr"] = int(card["CardNr"])
        card["Set"] = int(card["Set"])
        passedValues = passedValues.append(card, ignore_index=True)
    else:
        counted = False
        for jndex, subcards in passedValues.loc[passedValues['Card'] == card["Card"]].iterrows():
            if card.drop(["Amount", "Ebay price"]).tolist() == subcards.drop(["Amount", "Ebay price"]).tolist():
                passedValues.loc[jndex, "Amount"] += card["Amount"]
                counted = True
                break
        if not counted:
            passedValues = passedValues.append(card, ignore_index=True)

passedValues = passedValues.sort_values(["Set","CardNr"],ascending=[True,True])
passedValues = passedValues.drop(["CardNr","Set"], axis=1)

passedValues.to_csv('../data/pokemonsheet/1999formatted.csv', index=False)
