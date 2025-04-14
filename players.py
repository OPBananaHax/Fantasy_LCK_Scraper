players_dict = {'Clear': 6466, 'Raptor': 5659, 'VicLa': 4714, 'Diable': 3907, 'Kellin': 4912, 'DuDu': 9021, 'Pyosik': 6570, 'BuLLDoG': 9450, 'Berserker': 9725, 'Life': 4014, 'Siwoo': 8709, 'Lucid': 9416, 'ShowMaker': 6721, 'Aiming': 468, 'BeryL': 3544, 'Rich': 3161, 'Sponge': 6396, 'Ucal': 4066, 'Teddy': 4489, 'Andil': 4832, 'Kiin': 7751, 'Canyon': 6408, 'Chovy': 2189, 'Ruler': 9410, 'Duro': 3964, 'Zeus': 8073, 'Peanut': 8755, 'Zeka': 807, 'Viper': 5060, 'Delight': 5100, 'PerfecT': 944, 'Cuzz': 2320, 'Bdd': 643, 'deokdam': 7311, 'Way': 4135, 'Kingen': 8018, 'GIDEON': 1808, 'Fisher': 5630, 'Jiwoo': 7760, 'Lehends': 4293, 'Morgan': 2843, 'HamBak': 4511, 'Clozer': 7447, 'Hype': 7901, 'Pollu': 7598, 'Doran': 9018, 'Oner': 5715, 'Faker': 4606, 'Gumayusi': 6678, 'Smash': 7298, 'Keria': 7799, 'Soboro': 3962, 'Willer': 8392, 'Wonjin': 364, 'Daystar': 9171, 'Envyy': 1742, 'Career': 6874, 'Lancer': 3111, 'DDoiV': 7535, 'Pungyeon': 3728, 'Slayer': 9875, 'Quantum': 8163, 'Minous': 2052, 'Jaehyuk': 5141, 'Sharvel': 263, 'Garden': 206, 'Wayne': 3506, 'Thumb': 8875, 'Berr': 8198, 'Frog': 6828, 'Juhan': 7848, 'kyeahoo': 8672, 'LazyFeel': 4457, 'Pleata': 8358, 'Hanbyeol': 5879, 'Wet': 9308, 'Kemish': 1388, 'About': 9089, 'Namgung': 5014, 'SIRIUSS': 8702, 'Rooster': 2841, 'Grizzly': 6763, 'Jackal': 6092, 'Tempester': 6532, 'Pyeonsik': 1194, 'Bluffing': 1727, 'Casting': 2774, 'Sero': 4232, 'YoungJae': 5142, 'Zinie': 412, 'Paduck': 8997, 'Peter': 741, 'Kangin': 7624, 'Sylvie': 7865, 'Carim': 2776, 'Calix': 547, 'vital': 2694, 'Crack': 340, 'Lonely': 2533, 'Ellim': 7585, 'Starlit': 763, 'Bull': 649, 'Levy': 985, 'Kice': 7337, 'HaeTae': 4090, 'Vincenzo': 8579, 'Poby': 696, 'Guti': 1918, 'Cypher': 4471, 'Cloud': 1184}
players_dict = {k.lower(): v for k, v in players_dict.items()}

def get_id(name):

    name = name.lower()
    if name in players_dict:
        return players_dict[name]

    return -1

