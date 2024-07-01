"""
* Name: Emerson Goss
* Date: 2/20/24
* Fantasy LCK
* Description: This program will retrieve data from gol.gg to populate a table
               of player stats. It scrapes team rosters and match stats from
               gol.gg league tabs and stores them in a dataframe with the
               following format:
                    Player (index) | Position | Team | Kills | Deaths | Assists | CS | GR
               This dataframe will then be saved to a csv file
"""
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import pickle
import ssl

# these are the urls on gol.gg for the list of matches and the list of teams by ranking in LCK
#   matchlist url is used to access games played for player stats
#   rankings url is used to access team rosters for storing stats in a dataframe
matchlist_url = 'https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202024/'
rankings_url = 'https://gol.gg/tournament/tournament-ranking/LCK%20Summer%202024/'
folder_path = r'/Users/justynshelby/Documents/Programming/LCKScraper/rawstats.csv'

# force creation of a new file. False is default
# This will break the format if ran with force_weeks
force_restart = False
# force week - None or list of week numbers. None is default
# Will not update last updated values
force_weeks = None

def main():
    
    # fix ssl issue
    # something I found online to bypass scraping verification errors
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    # Restore/Create df
    if force_restart:
        df = new_df()
    else:
        try:
            df = pd.read_csv(folder_path, index_col=0)
            df = df_to_int(df)
        except FileNotFoundError:
            print("rawstats.csv not found. Creating file...")
            df = new_df()

    # Determine which weeks to scrape
    if force_weeks:
        for i in range(len(force_weeks)):
            force_weeks[i] -= 1
        weeks = list(zip(force_weeks, [0] * len(force_weeks)))
        for week in weeks:
            df, r = get_week_matches(week, df, strict=True)
            if r == 1:
                # Week is incomplete, update and save
                df.iloc[0, 1] = int(week[0] + 1)
                df.iloc[0, 2] = int(i)
                break

    else:
        week = (max(df.iloc[0, 1] - 1, 0), df.iloc[0, 2])
        df, r = get_week_matches(week, df)
        if r != 0:
            # Week is incomplete, update and save
            df.iloc[0, 1] = int(r[0])
            df.iloc[0, 2] = int(r[1])
        else:
            # Week is complete, set to next week match 0
            df.iloc[0, 1] = int(r[0] + 1)
            df.iloc[0, 2] = int(0)

    # Save df
    df.to_csv(folder_path)

def new_df():

    columns = ["playername", "kills", "deaths", "assists", "cs", "week", "matchnum", "gamenum"]
    df = pd.DataFrame(columns=columns)
    df.loc[0] = [None] + [int(0)] * (len(columns) - 1)
    df = df_to_int(df) 
    return df

def df_to_int(df):
    df = df.astype({"kills": "int",
                    "deaths": "int",
                    "assists": "int",
                    "cs": "int",
                    "week": "int",
                    "matchnum": "int",
                    "gamenum": "int"})
    return df

def get_week_matches(week, df, strict=False):

    soup = use_soup(matchlist_url)
    rows = soup.find_all('tr')
    match_rows = rows[1:]
    match_rows.reverse()
    first_match = int(week[0]) * 10
    
    # Set to a finite number to avoid infinite loops in case of failure
    end_count = 10 if strict else 100
    for i in range(week[1], end_count):

        # columns are as follows:
        #   Match link - team1 - score - team2 - week - patch - date
        if first_match + i >= len(match_rows):
            return df, [week[0], 0]
        row = match_rows[first_match + i]
        print(f"Scraping {row.find('td').get_text()} ", end='')
        cols = row.find_all('td')

        # Get match link
        match_url = find_href_link(cols[0].contents[0])

        # use get_stats function to input player stats into stats_df
        r = get_match_stats(int(week[0]) + 1 + i // 10, match_url, i % 10, df)
        if r[1] == 1:
            # No match, break
            print("- has yet to occur! Stopping...")
            return df, [int(week[0]) + 1 + i // 10, i % 10]
        df = r[0]
        
    return df, 0

def get_match_stats(week, match_url, match_index, df):

    # go into the match url to find links to game 1 and game 2
    soup = use_soup(match_url)
    game_links = soup.find_all('li', class_="nav-item game-menu-button")

    # check that games have occurred, otherwise there will only be 1 or 2 links on the page
    if len(game_links) <= 2:
        return df, 1

    # loop through the lines of html for game 1 and 2 to get the link to the game stats
    #for game_line in game_links[1:3]:
    print(f"week {week} match {match_index}")
    for j in range(2):
        game_line = game_links[j + 1]
        game_url = find_href_link(game_line)
        soup = use_soup(game_url)
        #team1 = soup.find_all('div', attrs={"class":"col-12 blue-line-header"})
        #team2 = soup.find_all('div', attrs={:"col-12 red-line-header"})
        # players, kdas, and cs are all stored on unique lines identifiable by a unique tag and class or style
        players = soup.find_all('a', attrs={"class":"link-blanc"})
        kdas = soup.find_all('td', attrs={"style":"text-align:center"})
        cs = soup.find_all('td', attrs={"style":"text-align:center;"})

        # check that there are only 10 players and statlines
        assert len(players) == 10
        assert len(kdas) == 10
        assert len(cs) == 10
        
        for i in range(10):
            player = players[i].contents[0]
            kdacs = convert_kda(kdas[i].contents[0], cs[i].contents[0])
            new_row = {"week": int(week),
                       "matchnum": int(match_index),
                       "gamenum": int(j),
                       "playername": player,
                       "kills": int(kdacs[0]),
                       "deaths": int(kdacs[1]),
                       "assists": int(kdacs[2]),
                       "cs": int(kdacs[3])}
            index = 200 * (week - 1) + 20 * match_index + 10 * j + i + 1
            if len(df) > index:
                df.iloc[index] = new_row
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df, 0

### HELPER FUNCTIONS ###
def use_soup(url):
    # This function uses BeautifulSoup to read in a url
    # it includes a header to avoid potential 403 errors
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    # Return a beautiful soup object
    return soup

def find_href_link(html_line, team=False):
    # This function takes in a line of html containing an href navigation link
    # and it returns the href link url as a string
    # line has format of <tag class..... href="link_url" title.... tag>
    line = str(html_line)
    for i in range(len(line)):
        # search for href=" that comes before url
        if line[i:i+6] == 'href="':
            # find index of h in href
            url_start_ind = i + 6   # store index of first character in url
            break
    # store the url in a string
    url = ""
    # add every next letter into the url until reaching '" ' that comes after
    # the end of the url in html format
    for i in range(url_start_ind, len(line)):
        if line[i] == '"':
            break
        else:
            url += line[i]
    # url tends to start with .. in reference to base website homepage
    # actual url = https://gol.gg + "../game/stats/#####/page-summary/"
    if url[0] == '.':
        if team:
            full_url = "https://gol.gg/teams" + url[1:]
        else:
            full_url = "https://gol.gg" + url[1:]
        return full_url
    else:
        return url

def convert_kda(kda_string, cs):
    # takes in a player's kda and cs in the form of 'K/D/A' and ' cs#' and
    # converts it into a list of integers with the form [K, D, A, cs] 
    div = []
    div_found = 0
    # loop through the kda string, recording the index of each / and ending
    # once two have been found - one between KD and one between DA
    for i in range(len(kda_string)):
        if kda_string[i] == "/":
            div.append(i)
            div_found += 1
        if div_found >= 2:
            break
    # kills is the number before first /
    kills = int(kda_string[:div[0]])
    # deaths is the number between both /
    deaths = int(kda_string[div[0]+1:div[1]])
    # assists is the number after last /
    assists = int(kda_string[div[1]+1:])
    # cs can just be converted into an integer, removing any extra spaces
    cs = int(cs)
    return [kills, deaths, assists, cs]

if __name__ == '__main__':
    main()

