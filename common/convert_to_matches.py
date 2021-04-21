import pandas as pd

matches = pd.DataFrame({
    'Team': pd.Series([], dtype='category'),
    'Opponent': pd.Series([], dtype='category'),
    'Goals': pd.Series([], dtype='int'),    # Goals scored
    'GA': pd.Series([], dtype='int'),       # Goals against
    'Home': pd.Series([], dtype='bool'),
    'Overtime': pd.Series([], dtype='category'),     # NaN, OT, SO, 2OT, etc.
    'Date': pd.Series([], dtype='datetime64[ns]'),
    'Season': pd.Series([], dtype='category'),
    'Type': pd.Series([], dtype='category')
})

def convert_to_matches(df, team, opponent=None):
    # filter to home and away games
    if opponent is None:
        home = df.loc[df['Home'] == team].drop(columns=['Attendance', 'Length', 'Notes'])
        away = df.loc[df['Visitor'] == team].drop(columns=['Attendance', 'Length', 'Notes'])
    else:
        home = df.loc[(df['Home'] == team) & (df['Visitor'] == opponent)].drop(columns=['Attendance', 'Length', 'Notes'])
        away = df.loc[(df['Visitor'] == team) & (df['Home'] == opponent)].drop(columns=['Attendance', 'Length', 'Notes'])
    # rename home to match
    home = home.rename(columns={'Home':'Team', 'Visitor':'Opponent', 'Home Goals':'Goals', 'Visitor Goals':'GA'}, inplace=False)
    home['Home'] = True
    # rename away to match
    away = away.rename(columns={'Visitor':'Team', 'Home':'Opponent', 'Home Goals':'GA', 'Visitor Goals':'Goals'}, inplace=False)
    away['Home'] = False
    # return combined sorted by date
    return pd.concat([matches, home, away], ignore_index=True).sort_values('Date')