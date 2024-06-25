"""
* Name: Emerson Goss
* Date: 2/20/24
* Independent Project: Fantasy LOL
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

# something I found online to bypass scraping verification errors
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# Completed
def use_soup(url):
    # This function uses BeautifulSoup to read in a url
    # it includes a header to avoid potential 403 errors
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")
    # Return a beautiful soup object
    return soup

# Completed
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

# Completed
def convert_week_string(week_label):
    # This function takes in the week of a match as listed on gol.gg and
    # converts it into a cleaner version as a string
    # week_label can look like:
    #       WEEK1 / WEEK 3...
    #       TIEBREAKER      (this should result in a skip)
    found_week = False
    for i in range(len(week_label)):
        # Search in the string for 'WEEK'
        if week_label[i:i+4] == "WEEK":
            # Convert to 'Week x' and return
            return("Week " + week_label[i+4])
    # if no 'WEEK#' is found, just return skip
    return("Skip")

# Completed
def get_team_rosters(team_url):
    # Create a list of lists containing the players and roles of the format:
    #   [[Doran, TOP], [Peanut, JUNGLE], [Zeka, MID]...]
    roster_list = []
    soup = use_soup(team_url)
    # rosters are stored in the last table under tag 'tbody'
    tb = soup.find_all('tbody')
    player_table = tb[-1]
    # player_list contains each line in the roster table
    p1 = player_table.tr
    p2 = p1.find_next_siblings('tr')
    player_list = [p1] + p2
    # if there are more than 5 players (ie. subs), remove the 1st and 6th line denoting
    # the 'last used roster' and 'substitutes' labels
    if len(player_list) > 5:
        player_list.pop(6)
        player_list.pop(0)
    # player's role is the text in the 1st column and their ign is the text in the 2nd column
    for player in player_list:
        role_line = player.td
        p_role = str(role_line.text)
        # remove space before role (ie. ' TOP' --> 'TOP')
        p_role = [p_role.replace(' ', '')]
        name_line = role_line.find_next_sibling('td')
        p_name = str(name_line.text)
        # remove \xa0 (non-breaking space) from player name
        p_name = [p_name.replace(u'\xa0', u'')]
        pair = p_name + p_role
        # add [player name, player role] to the roster list
        roster_list.append(pair)
    return roster_list

# Completed
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

# Completed
def get_team_abbr(team_name):
    # store the team names and their abbreviations in a dictionary
    team_abbr = {'T1':'T1',
            'KT Rolster':'KT',
            'Kwangdong Freecs':'KDF',
            'FearX':'FOX',
            'OK BRION':'BRO',
            'DRX':'DRX',
            'Hanwha Life eSports':'HLE',
            'Dplus KIA':'DK',
            'Nongshim RedForce':'NS',
            'Gen.G eSports':'GEN'}
    return team_abbr[team_name]

# Completed
def get_game_stats(game_url, df):
    # This function takes in a game page url on gol.gg and returns a
    # dataframe with updated player stats for the match played
    soup = use_soup(game_url)
    #team1 = soup.find_all('div', attrs={"class":"col-12 blue-line-header"})
    #team2 = soup.find_all('div', attrs={"class":"col-12 red-line-header"})
    # players, kdas, and cs are all stored on unique lines identifiable 
    # by a unique tag and class or style
    players = soup.find_all('a', attrs={"class":"link-blanc"})
    kdas = soup.find_all('td', attrs={"style":"text-align:center"})
    cs = soup.find_all('td', attrs={"style":"text-align:center;"})
    # check that there are only 10 players and statlines
    assert len(players) == 10
    assert len(kdas) == 10
    assert len(cs) == 10
    # for each player add their kills, deaths, assists, and cs to their current
    # value in the week's dataframe
    for i in range(10):
        player = players[i].contents[0]
        kdacs = convert_kda(kdas[i].contents[0], cs[i].contents[0])
        df.loc[player, 'Kills'] += kdacs[0]
        df.loc[player, 'Deaths'] += kdacs[1]
        df.loc[player, 'Assists'] += kdacs[2]
        df.loc[player, 'CS'] += kdacs[3]
    return df

# Completed
def get_match_stats(match_url, df, match_name):
    # go into the match url to find links to game 1 and game 2
    soup = use_soup(match_url)
    game_links = soup.find_all('li', class_="nav-item game-menu-button")
    # check that games have occurred, otherwise there will only be 1 or 2 links on the page
    if len(game_links) <= 2:
        print('match has not occurred yet')
        return df, match_name
    # loop through the lines of html for game 1 and 2 to get the link to the game stats
    for game_line in game_links[1:3]:
        game_url = find_href_link(game_line)
        # update the stats dataframe with the game stats
        df = get_game_stats(game_url, df)
    return df, 'Completed'

# Completed
def get_week_matches(matchlist_url, week_num, stats_df):
    soup = use_soup(matchlist_url)
    rows = soup.find_all('tr')
    # Skip the first 'tr' tag as it is not in a match row
    match_rows = rows[1:]
    # Reverse order to start with first matches that were played
    match_rows.reverse()
    curr_week = 0
    i = 0
    # Iterate through each row to find the matches from desired week
    while (curr_week <= week_num) and (i < len(match_rows)):
        row = match_rows[i]
        # columns are as follows:
        #   Match link - team1 - score - team2 - week - patch - date
        cols = row.find_all('td')
        # Get a 'Week X' string to keep track of where we are in the matchlist
        week_str = cols[4].contents[0]
        week_key = convert_week_string(week_str)
        curr_week = int(week_key[5])
        # There are 10 matches (rows) each week so jump by 10 if in wrong week
        if curr_week < week_num:
            i += 10
        elif curr_week == week_num:
            # Get match link and team names
            match_url = find_href_link(cols[0].contents[0])
            teams = [get_team_abbr(cols[1].contents[0]), get_team_abbr(cols[3].contents[0])]
            match_name = teams[0] + ' vs ' + teams[1]
            print(match_name)
            print()
            # use get_stats function to input player stats into stats_df
            stats_df, final_match = get_match_stats(match_url, stats_df, match_name)
            for team in teams:
                # subtracts 2 from GR value for all players in a team regardless if the player participated in that match
                stats_df.loc[stats_df['Team'] == team, ['GR']] -= 2
            if final_match != 'Completed':
                return stats_df, final_match
            i += 1
    return stats_df, final_match

# Completed
def initial_rosters(rankings_url):
    # This function uses the team rankings url on gol.gg to get team rosters
    # It creates 3 lists of equal length containing:
    #   player name                     ['Kiin', 'Canyon', 'Chovy', 'Peyz', 'Lehends', 'Zeus', ...]
    #   team name for that player       ['GEN', 'GEN','GEN','GEN','GEN', 'T1', ...]
    #   player position                 ['TOP', 'JUNGLE', 'MID', 'ADC', 'SUP', 'TOP', ...]
    players_list = []
    teams_list = []
    position_list = []

    soup = use_soup(rankings_url)
    tb = soup.find_all('tbody')
    # Each row of team data has tag 'tr'
    tr1 = tb[0].tr
    trn = tr1.find_next_siblings('tr')
    trs = [tr1] + trn
    # loop through each row of team data and get the team name
    # and link to their roster
    for team in trs:
        col1 = team.td
        team_name = col1.text
        team_name = get_team_abbr(team_name)
        team_link = find_href_link(col1)
        # get list of [player1, player2, player3...] and [player1 role, player2 role, player3 role...]
        print('starting on ' + str(team_name))
        roster, roles = get_team_rosters(team_link)
        assert(len(roster) == len(roles))
        for i in range(len(roster)):
            teams_list.append(team_name)
        players_list += roster
        position_list += roles
        
    return players_list, position_list, teams_list

# Completed
def get_team_rosters(team_url):
    soup1 = use_soup(team_url)
    all_url_line = soup1.find_all('a', attrs={"class":"lien_region"})
    all_url = find_href_link(all_url_line, True)

    # Create a list of lists containing the players and roles of the format:
    #   [[Doran, TOP], [Peanut, JUNGLE], [Zeka, MID]...]
    roster_list = []
    roles_list = []
    soup = use_soup(all_url)
    # rosters are stored in the last table under tag 'tbody'
    tb = soup.find_all('tbody')
    player_table = tb[-1]
    # player_list contains each line in the roster table
    p1 = player_table.tr
    p2 = p1.find_next_siblings('tr')
    player_list = [p1] + p2
    # if there are more than 5 players (ie. subs), remove the 1st and 6th line denoting
    # the 'last used roster' and 'substitutes' labels
    if len(player_list) > 5:
        player_list.pop(6)
        player_list.pop(0)
    # player's role is the text in the 1st column and their ign is the text in the 2nd column
    for player in player_list:
        role_line = player.td
        p_role = str(role_line.text)
        # remove space before role (ie. ' TOP' --> 'TOP')
        p_role = p_role.replace(' ', '')
        name_line = role_line.find_next_sibling('td')
        p_name = str(name_line.text)
        # remove \xa0 (non-breaking space) from player name
        p_name = p_name.replace(u'\xa0', u'')
        # add player name and player role to the roster and role lists
        roster_list.append(p_name)
        roles_list.append(p_role)
    return roster_list, roles_list

# Completed
def generate_template_week_stats_df(rankings_url):
    # this function uses rankings url on gol.gg to get all players rostered by each team and
    #   creates a dataframe of the format:
    #       Player  Position    Team    Kills   Deaths  Assists CS  GR
    # scrape team rosters from rankings website to generate lists of players, their positions, and their teams
    players_list, position_list, teams_list = initial_rosters(rankings_url)
    # make sure each list is the same length so one index across each list refers to one player
    assert len(players_list) == len(position_list)
    assert len(players_list) == len(teams_list)
    # create empty lists to store games remaining (starting from 4) and game scores (starting from 0)
    GR_list = [4 for i in range(len(players_list))]
    KDACS_list = [0 for i in range(len(players_list))]
    # create a dictionary containing lists for each column and convert into a dataframe
    stats_dict = {'Player' : players_list,
                'Position' : position_list,
                'Team' : teams_list,
                'Kills' : KDACS_list,
                'Deaths' : KDACS_list,
                'Assists' : KDACS_list,
                'CS' : KDACS_list,
                'GR' : GR_list}
    df = pd.DataFrame(stats_dict)
    return  df  

# Completed
def get_template(first_time):
    if first_time:
        # call function to create weekly df of players rostered so far
        # df has format:
        #   Player  Position    Team    Kills   Deaths  Assists CS  GR
        df = generate_template_week_stats_df(rankings_url)
        df.index = df['Player']
        # save the dataframe as 'Template Week Stats.csv' to be accessed and read later on when filling in week scores
        df.to_csv(folder_path + '\Template Week Stats.csv', index=False)
    else:
        # can also read in the saved template dataframe
        df = pd.read_csv(r'C:\Users\thewa\.vscode\Python Projects\Template Week Stats.csv')
        df.index = df['Player']
    return df


# these are the urls on gol.gg for the list of matches and the list of teams by ranking in LCK
#   matchlist url is used to access games played for player stats
#   rankings url is used to access team rosters for storing stats in a dataframe
matchlist_url = 'https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202024/'
rankings_url = 'https://gol.gg/tournament/tournament-ranking/LCK%20Summer%202024/'
folder_path = r'C:\Users\thewa\.vscode\Python Projects'

# set first_time to true if you want to create a new template csv of player data
#   you should do this if new players have been added to LCK rosters, but isn't necessary
first_time = False
# set this to the week you want stats from
week_num = 1


df = get_template(first_time)
df, final_match = get_week_matches(matchlist_url, week_num, df)
if final_match != 'Completed':
    final_match = 'until ' + final_match
filename = 'Week ' + str(week_num) + ' Stats ' + final_match + '.csv'
df.to_csv(folder_path + '\\' + filename, index= False)
