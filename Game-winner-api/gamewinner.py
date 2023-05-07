from datetime import datetime, date, timedelta
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import scoreboardv2

def fetch_nba_results(date=None):
    if date is None:
        date = datetime.now() - timedelta(days=1)
    date_string = date.strftime('%m/%d/%Y')
    # else:
    #     date_string = date

    gamefinder = scoreboardv2.ScoreboardV2(day_offset=0, game_date=date_string)
    games = gamefinder.line_score.get_data_frame()

    winners = games.groupby('GAME_ID').apply(get_winner)
    # winners = winners.reset_index()


    return winners

def get_winner(group):
    points = group['PTS'].idxmax()
    winner = group.loc[points, ['GAME_ID', 'GAME_DATE_EST', 'GAME_SEQUENCE', 'TEAM_ID', 'TEAM_WINS_LOSSES']]
    return winner




# Example usage:
results = fetch_nba_results()
