### THIS SCRIPT WILL DEFINE FUNCTIONS FOR DATA COLLECTION USED IN NOTEBOOK 01

# import libraries
import pandas as pd
import time
import nba_api as nba
from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashteamstats



# define a function to scrape mvp shares from 2000 to 2026
def get_mvp_shares():

    # initialize range of all applicable seasons
    seasons = range(2000, 2027)

    # initialize empty list to store dfs
    mvp_shares_list = []

    # get mvp shares table for all seasons
    for season in seasons:

        # bbr awards url
        bbr_url = f'https://www.basketball-reference.com/awards/awards_{season}.html'

        # read in the tables from that url
        tables = pd.read_html(bbr_url)

        # extract the mvp table
        mvp_shares = tables[0]
        mvp_shares = mvp_shares.reset_index(drop=True)

        # flatten dataframe
        mvp_shares.columns = ['_'.join(col) for col in mvp_shares.columns]

        # keep only necessary columns
        mvp_shares = mvp_shares[['Unnamed: 0_level_0_Rank', 'Unnamed: 1_level_0_Player', 'Unnamed: 3_level_0_Tm',
                                'Voting_First', 'Voting_Pts Won', 'Voting_Pts Max', 'Voting_Share' ]]

        # rename columns for readability
        mvp_shares = mvp_shares.rename(columns = {'Unnamed: 0_level_0_Rank': 'Rank',
                                        'Unnamed: 1_level_0_Player': 'Player Name',
                                        'Unnamed: 3_level_0_Tm': 'Team',
                                        'Voting_First': 'First Place Votes',
                                        'Voting_Pts Won': 'Total Voting Points',
                                        'Voting_Pts': 'Max Voting Points',
                                        'Voting_Share': 'MVP Share'})
        
        # add season column
        mvp_shares['Season'] = season

        # add df to list
        mvp_shares_list.append(mvp_shares)

    # concat all dfs into a single dataframe
    merged_mvp_shares = pd.concat(mvp_shares_list, ignore_index = True)

    return merged_mvp_shares


# define a function to pull season-level player stats from 2000 to 2027
def get_player_stats():

    # initialize range of all applicable seasons
    seasons = range(2000, 2027)

    # initialize a list to store player dfs
    player_stat_dfs = []

    # iterate through each season and pull all player stats where the player plays at least 50 games and averaged 20 mpg
    for season in seasons:

        # begin iterations
        print(f"Pulling season {season}...")

        # create an acceptably formatted season string
        season_str = f'{season-1}-{str(season)[-2:]}'

        # extract season-level data
        player_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season_str, timeout=60).get_data_frames()[0]

        # add season column
        player_stats['Season'] = season


        # keep only relevant columns
        player_stats = player_stats[['Season', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION',
                                     'GP', 'W', 'L', 'MIN',
                                    'PTS', 'REB', 'AST', 'STL', 'BLK',
                                    'PTS_RANK', 'REB_RANK', 'AST_RANK', 'PLUS_MINUS_RANK',
                                    'FG_PCT', 'FG3_PCT', 'FT_PCT', 'PLUS_MINUS']]
        

        
        # filter out all players that played less than 50 games or played less than 20 min per game
        player_stats = player_stats[(player_stats['MIN'] / player_stats['GP'] >= 20) & (player_stats['GP'] >= 50)]

        # append to list
        player_stat_dfs.append(player_stats)

        time.sleep(2)

        

    # concat all dfs
    merged_player_stats = pd.concat(player_stat_dfs, ignore_index=True)

    return merged_player_stats


# define a function to pull season-level team stats from 2000 to 2027
def get_team_stats():

    # initialize range of all applicable seasons
    seasons = range(2000, 2027)

    # initialize a list to store player dfs
    team_stat_dfs = []

    # iterate through each season and pull all player stats where the player plays at least 50 games and averaged 20 mpg
    for season in seasons:

        # begin iterations
        print(f"Pulling team stats for {season} season...")

        # create an acceptably formatted season string
        season_str = f'{season-1}-{str(season)[-2:]}'

        # extract season-level data
        team_stats = leaguedashteamstats.LeagueDashTeamStats(season=season_str, timeout=10).get_data_frames()[0]

        # add season column
        team_stats['Season'] = season


        # keep only relevant columns
        team_stats = team_stats[['Season', 'TEAM_ID', 'TEAM_NAME',
                                     'W', 'L', 'W_PCT', 'W_RANK', 'W_PCT_RANK']]

        # append to list
        team_stat_dfs.append(team_stats)

        # add sleep to stop from timing out
        time.sleep(2)

        

    # concat all dfs
    merged_team_stats = pd.concat(team_stat_dfs, ignore_index=True)

    return merged_team_stats


