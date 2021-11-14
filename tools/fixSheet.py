import pandas as pd
import time as t

indexedCards = pd.read_csv("../data/pokemonsheet/pokemonSheet.csv").drop(["File Name","Mavin Price","Troll&Toad Price","Subtotal"],axis=1)
passedValues = pd.DataFrame(columns=list(indexedCards.columns))

for index, card in indexedCards.iterrows():
    if not card["Card"] in passedValues["Card"].tolist():
        passedValues = passedValues.append(card,ignore_index=True)
    else:
        counted=False
        for jndex, subcards in passedValues.loc[passedValues['Card'] == card["Card"]].iterrows():
            if card.drop(["Amount","Ebay price"]).tolist() == subcards.drop(["Amount","Ebay price"]).tolist():
                passedValues.loc[jndex,"Amount"]+=card["Amount"]
                counted=True
                break
        if not counted:
            passedValues = passedValues.append(card,ignore_index=True)
passedValues.to_csv('../data/pokemonsheet/improvedPokemonSheets.csv', index=False)