import streamlit as st

import numpy as np
import pandas as pd
from common import convert_to_matches, prematch_stats

scores = pd.read_pickle('data/scores.pkl')
teams = sorted(scores['Visitor'].unique().to_list())


st.title('NHL Matchups')

home_team = st.selectbox('Select the home team:', teams)
away_team = st.selectbox('Select the away team:', teams, index=1)


if st.button('Run'):
    result = convert_to_matches(scores, home_team, away_team)

    st.write('Here are games between the two over the past seasons:')
    st.table(result.astype('object').assign(hack='').set_index('hack'))