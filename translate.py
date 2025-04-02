import pandas as pd
from Fantasy_LOL_Center import df_to_int
from players import get_id

folder_path = r'/Users/justynshelby/Documents/Programming/LCKScraper/rawstats.csv'
# Updated last visited location. Deafult True
# Automatically false if force is true
update_loc = True
# Dictionary of week match pairs, or false. Default false
force_matches = False
# Create undo queries to rollback a change. Default is false
undo = False

def main():

    try:
        df = pd.read_csv(folder_path, index_col=0)
        df = df_to_int(df)
    except FileNotFoundError:
        print("rawstats.csv not found. Please run scraper first. Exiting ")
        return 1

    #week, match = max(df.iloc[0, 3] - 1, 0), df.iloc[0, 4]
    week, match = 7, 0
    index = 200 * week + 20 * match
 
    stats = {}
    while len(df) > index + 1:
        for i in range(1, 21):
            data = df.loc[index + i]
            id = get_id(data["playername"])
            if id == -1:
                print(f"{data['playername']} not in database")
                return 1
            if id in stats and stats[id]["week"] == week + 1:
                stats[id]["kills"] += data["kills"]
                stats[id]["deaths"] += data["deaths"]
                stats[id]["assists"] += data["assists"]
                stats[id]["cs"] += data["cs"]
                points = round(data["kills"] * 2 + data["assists"] * 1.5 + data["cs"] * 0.01 - data["deaths"] * 0.5, 2)
                stats[id]["points"] += points
                stats[id]["gamesPlayed"] += 1
            else:
                if week + 1 == 8:
                    points = round(data["kills"] * 2 + data["assists"] * 1.5 + data["cs"] * 0.01 - data["deaths"] * 0.5, 2)
                    stats[id] = {"kills": data["kills"],
                               "deaths": data["deaths"],
                               "assists": data["assists"],
                               "cs": data["cs"],
                               "points": points,
                               "gamesPlayed": 1,
                               "week": week + 1}
                    print(f"checking location {index + i}, {stats[id]}")
        index += 20
        match += 1 
        if match >= 10:
            week += 1 
            match = 0

    for id, stat in stats.items():
        sign = "+" if not undo else "-"
        print(f"UPDATE Stats SET kills = kills {sign} {stat['kills']}, deaths = deaths {sign} {stat['deaths']}, assists = assists {sign} {stat['assists']}, cs = cs {sign} {stat['cs']}, points = ROUND(points {sign} {stat['points']}, 2), gamesPlayed = gamesPlayed {sign} {stat['gamesPlayed']} WHERE playerID = {id} AND week = {stat['week']};")

    if force_matches == False and update_loc:
        df.iloc[0, 3] = week + 1 
        df.iloc[0, 4] = match

    df.to_csv(folder_path)

if __name__ == '__main__':
    main()

