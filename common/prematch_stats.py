import pandas as pd
from common import convert_to_matches

def prematch_stats(df, team, opponent):
    data = convert_to_matches(df , team, opponent)
    # for season, data in df.groupby('Season'):
    # wins
    wins = sum(data['Goals'] > data['GA'])
    home_wins = sum((data['Goals'] > data['GA']) & data['Home'])
    away_wins = wins - home_wins
    # losses
    losses = sum((data['Goals'] < data['GA']) & pd.isnull(data['Overtime']))
    home_losses = sum((data['Goals'] < data['GA']) & pd.isnull(data['Overtime']) & data['Home'])
    away_losses = losses - home_losses
    # overtime
    ot_losses = sum((data['Goals'] < data['GA']) & pd.notnull(data['Overtime']))
    home_ot_losses = sum((data['Goals'] < data['GA']) & pd.notnull(data['Overtime']) & data['Home'])
    away_ot_losses = ot_losses - home_ot_losses
    # other
    ot_wins = sum((data['Goals'] > data['GA']) & pd.notnull(data['Overtime']))
    so_losses = sum((data['Goals'] < data['GA']) & (data['Overtime'] == 'SO'))
    so_wins = sum((data['Goals'] > data['GA']) & (data['Overtime'] == 'SO'))

    print("Record: {}-{}-{}".format(wins, losses, ot_losses))
    print("Home Record: {}-{}-{}".format(home_wins, home_losses, home_ot_losses))
    print("Away Record: {}-{}-{}".format(away_wins, away_losses, away_ot_losses))