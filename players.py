players_dict = {
    "Kiin": {"id": 0, "role": "Top"},
    "Zeus": {"id": 1, "role": "Top"},
    "Doran": {"id": 2, "role": "Top"},
    "PerfecT": {"id": 3, "role": "Top"},
    "Kingen": {"id": 4, "role": "Top"},
    "DuDu": {"id": 5, "role": "Top"},
    "Clear": {"id": 6, "role": "Top"},
    "DnDn": {"id": 7, "role": "Top"},
    "Rascal": {"id": 8, "role": "Top"},
    "Morgan": {"id": 9, "role": "Top"},
    "Canyon": {"id": 10, "role": "Jng"},
    "Oner": {"id": 11, "role": "Jng"},
    "Peanut": {"id": 12, "role": "Jng"},
    "Pyosik": {"id": 13, "role": "Jng"},
    "Lucid": {"id": 14, "role": "Jng"},
    "Cuzz": {"id": 15, "role": "Jng"},
    "Willer": {"id": 16, "role": "Jng"},
    "Sylvie": {"id": 17, "role": "Jng"},
    "Sponge": {"id": 18, "role": "Jng"},
    "YoungJae": {"id": 19, "role": "Jng"},
    "Chovy": {"id": 20, "role": "Mid"},
    "Faker": {"id": 21, "role": "Mid"},
    "Zeka": {"id": 22, "role": "Mid"},
    "Bdd": {"id": 23, "role": "Mid"},
    "Showmaker": {"id": 24, "role": "Mid"},
    "BuLLDoG": {"id": 25, "role": "Mid"},
    "Clozer": {"id": 26, "role": "Mid"},
    "Fisher": {"id": 27, "role": "Mid"},
    "SeTab": {"id": 28, "role": "Mid"},
    "Karis": {"id": 29, "role": "Mid"},
    "Peyz": {"id": 30, "role": "ADC"},
    "Gumayushi": {"id": 31, "role": "ADC"},
    "Viper": {"id": 32, "role": "ADC"},
    "Deft": {"id": 33, "role": "ADC"},
    "Aiming": {"id": 34, "role": "ADC"},
    "Bull": {"id": 35, "role": "ADC"},
    "Hena": {"id": 36, "role": "ADC"},
    "Jiwoo": {"id": 37, "role": "ADC"},
    "Teddy": {"id": 38, "role": "ADC"},
    "Envyy": {"id": 39, "role": "ADC"},
    "Lehends": {"id": 40, "role": "Supp"},
    "Keria": {"id": 41, "role": "Supp"},
    "Delight": {"id": 42, "role": "Supp"},
    "BeryL": {"id": 43, "role": "Supp"},
    "Kellin": {"id": 44, "role": "Supp"},
    "Andil": {"id": 45, "role": "Supp"},
    "Execute": {"id": 46, "role": "Supp"},
    "Peter": {"id": 47, "role": "Supp"},
    "Pleata": {"id": 48, "role": "Supp"},
    "Pollu": {"id": 49, "role": "Supp"},
    "Mihile": {"id": 50, "role": "Top"},
    "Leaper": {"id": 51, "role": "ADC"},
    "Moham": {"id": 52, "role": "Supp"},
    "GuGer": {"id": 53, "role": "Supp"},
    "Raptor": {"id": 54, "role": "Jng"},
    "Casting": {"id": 55, "role": "Top"},
    "Samver": {"id": 56, "role": "ADC"},
    "kyeahoo": {"id": 57, "role": "Mid"},
    "Frog": {"id": 58, "role": "Top"},
    "Callme": {"id": 59, "role": "Mid"},
    "DDoiV": {"id": 60, "role": "Jng"},
    "Pullbae": {"id": 61, "role": "Mid"},
    "Duro": {"id": 62}
}

translate = {
    "kingen": "Kingen",
    "ShowMaker": "Showmaker",
    "Bulldog": "BuLLDoG"
}

def get_id(name):

    if name in translate:
        name = translate[name]

    if name in players_dict:
        return players_dict[name]["id"]

    return -1

