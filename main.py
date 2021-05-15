import streamlit as st

import numpy as np
import pandas as pd
from common import convert_to_matches, prematch_stats


def prematch_stats(data):
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

    record = "Record: {}-{}-{}\n".format(wins, losses, ot_losses)
    record += "Home Record: {}-{}-{}\n".format(home_wins, home_losses, home_ot_losses)
    record += "Away Record: {}-{}-{}\n".format(away_wins, away_losses, away_ot_losses)
    return record



scores = pd.read_pickle('data/scores.pkl')
teams = sorted(scores['Visitor'].unique().to_list())


st.title('NHL Matchups')

home_team = st.selectbox('Select the home team:', teams)
away_team = st.selectbox('Select the away team:', teams, index=1)


if st.button('Run'):
    scores = scores.loc[scores['Season'] == '2020-2021']
    result = convert_to_matches(scores, home_team, away_team)
    
    st.write("Record:")
    st.write(prematch_stats(result))

    st.write('Here are games between the two over the past seasons:')
    st.table(result.astype('object').assign(hack='').set_index('hack'))