import pandas as pd


class Scores(pd.DataFrame):

    def __init__(self, data, year) -> None:
        super().__init__(data=data)
        self.season = year
        self.playoffs = 'Playoffs' in self['Notes']
        self.teams = set(self['Home']).union(set(self['Visitor']))


    def get_record(self, team, opponent=None):

        # columns = ['Team', 'Games', 'Wins', 'Losses', 'OT Losses', 'Points', 'P%', 'OT Wins', 'Reg Win']
        team_dict = {'Team': team}

        # filter
        home_wins = self.loc[(self['Home']==team) & (self['Goals Home'] > self['Goals Visitor'])]
        away_wins = self.loc[(self['Visitor']==team) & (self['Goals Home'] < self['Goals Visitor'])]
        home_losses = self.loc[(self['Home']==team) & (self['Goals Home'] < self['Goals Visitor'])]
        away_losses = self.loc[(self['Visitor']==team) & (self['Goals Home'] > self['Goals Visitor'])]
        
        if opponent is not None:
            team_dict['Opponent'] = opponent
            home_wins = home_wins.loc[(self['Visitor']==opponent)]
            away_wins = away_wins.loc[(self['Home']==opponent)]
            home_losses = home_losses.loc[(self['Visitor']==opponent)]
            away_losses = away_losses.loc[(self['Home']==opponent)]

        wins = pd.concat([home_wins, away_wins], ignore_index=True)
        wins = wins.loc[(self['Notes'] != 'Playoffs')]

        losses = pd.concat([home_losses, away_losses], ignore_index=True)
        losses = losses.loc[(self['Notes'] != 'Playoffs')]

        # add to dict
        team_dict['Wins'] = len(wins)
        team_dict['OT Wins'] = len(wins.loc[~self['OT'].isnull()])
        team_dict['Reg Win'] = team_dict['Wins'] - team_dict['OT Wins']
        team_dict['Losses'] = len(losses.loc[self['OT'].isnull()])
        team_dict['OT Losses'] = len(losses) - team_dict['Losses']
        team_dict['Games'] = team_dict['Wins'] + team_dict['Losses'] + team_dict['OT Losses']
        team_dict['Points'] = 2 * team_dict['Wins'] + team_dict['OT Losses']
        team_dict['P%'] = round(team_dict['Points'] / team_dict['Games'], 4)    # FIXME

        return team_dict


    def get_standings(self):
        """ Compute the standings from the scores
        TODO: add conferences and divisions
        """
        standings = [self.get_record(team) for team in self.teams]
        standings = pd.DataFrame(standings).sort_values('P%', ascending=False)

        return standings

