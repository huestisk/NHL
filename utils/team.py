import pandas as pd 

# teams = sorted(matches['Team'].unique())

class Team():

    def __init__(self, name) -> None:
        self.name = name

    def get_matchup(self, scores, opponent):
        raise NotImplementedError

    def get_record(data, team):
        """ FIXME """
        raise NotImplementedError
        record = pd.DataFrame({
            'Opponent': pd.Series([], dtype='category'),
            'Self': pd.Series([], dtype='bool'),
            'Games': pd.Series([], dtype='int'),
            'Wins': pd.Series([], dtype='int'),
            'Losses': pd.Series([], dtype='int'),
            'OT Wins': pd.Series([], dtype='int'),
            'OT Losses': pd.Series([], dtype='int'),
            'Reg Win': pd.Series([], dtype='int'),
            'Goals': pd.Series([], dtype='int'),     # Goals scored
            'GA': pd.Series([], dtype='int'),        # Goals against
            'Season': pd.Series([], dtype='category')
        })
        # Add Teams
        record['Opponent'] = teams  #data['Team'].unique()
        record['Self'] = record['Opponent'] == team
        record['Season'] = (data['Season'].unique()).to_list()[0]
        # Fill zeros
        record = record.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc' else x)
        # Go through all of the games (FIXME: could be sped up)
        for _, row in data.loc[data['Team'] == team].iterrows():
            # get oppenent's position in the df
            idx = record.index[record['Opponent'] == row['Opponent']].tolist()[0]
            # count number of games
            record.at[idx, 'Games'] += 1
            # count wins, losses and OT
            if row['Goals'] > row['GA']:
                record.at[idx, 'Wins'] += 1
                if row['Overtime']:
                    record.at[idx, 'OT Wins'] += 1
            elif row['Overtime']:
                record.at[idx, 'OT Losses'] += 1
            else:
                record.at[idx, 'Losses'] += 1
            # count goals and goals against
            record.at[idx, 'Goals'] += row['Goals']
            record.at[idx, 'GA'] += row['GA']
        # compute goal difference
        record['Diff'] = record['Goals'] - record['GA']
        # compute regulation wins
        record['Reg Win'] = record['Wins'] - record['OT Wins']
        # display(record.sort_values('Opponent', ascending=False))
        return (record.sort_values('Opponent', ascending=False)).to_numpy()