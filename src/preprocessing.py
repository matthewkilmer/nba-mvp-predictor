### THIS SCRIPT CONTAINS ALL FUNCTION USED WITHIN NOTEBOOK 2

# import libraries
import pandas as pd

# define a function to map all team abbreviations to the correct team and to handle any misformatted/duplicate names
def map_team_names(player_stats, team_stats):

    # create a map for team abbreviations
    team_abb_to_name = {
    'ATL': 'Atlanta Hawks',
    'BKN': 'Brooklyn Nets',
    'BOS': 'Boston Celtics',
    'CHA': 'Charlotte Hornets',
    'CHH': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'LA Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NJN': 'Brooklyn Nets',
    'NOH': 'New Orleans Pelicans',
    'NOK': 'New Orleans Pelicans',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'SEA': 'Oklahoma City Thunder',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'VAN': 'Memphis Grizzlies',
    'WAS': 'Washington Wizards'
    }

    # create a dict to clean up normalize names
    team_name_normalized = {
    'LA Clippers': 'LA Clippers',
    'Los Angeles Clippers': 'LA Clippers',
    'New Jersey Nets': 'Brooklyn Nets',
    'Charlotte Bobcats': 'Charlotte Hornets',
    'Seattle SuperSonics': 'Oklahoma City Thunder',
    'Vancouver Grizzlies': 'Memphis Grizzlies',
    'New Orleans Hornets': 'New Orleans Pelicans',
    'New Orleans/Oklahoma City Hornets': 'New Orleans Pelicans',
    }

    # use dicts to map
    player_stats['TEAM_NAME'] = player_stats['TEAM_ABBREVIATION'].map(team_abb_to_name)
    team_stats['TEAM_NAME'] = team_stats['TEAM_NAME'].replace(team_name_normalized)