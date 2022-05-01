import pandas as pd

from requests import get
from datetime import datetime
from bs4 import BeautifulSoup as soup

FLAGS = {   # FIXME: remove to yaml
    '1' : "Sweden",
    '2' : "Finland",
    '3' : "Canada",
    '4' : "Slovakia",
    '5' : "Norway",
    '6' : "USA",
    '7' : "Denmark",
    '8' : "Czech",
    '9' : "Russia",
    '10': "Switzerland",
    '11': "Latvia",
    '12': "Austria",
    '20': "Japan",
    '21': "Germany",
    '23': "Belarus",
    '25': "England",
}


class Scraper():

    def __init__(self) -> None:
        pass


    def scrape_scores_by_season(self, year, season=None, playoffs=None) -> pd.DataFrame:
        ''' Read scores from website 
        TODO: add functionality to detect errors
        FIXME: currently tables are hard coded
        '''
        if season or (season is None and not playoffs):
            try:
                url = f'https://www.hockey-reference.com/leagues/NHL_{year}_games.html'

                response = get(url)
                html = soup(response.text, 'html.parser')
                div = html.find(id='div_games')

                df_season = pd.read_html(str(div))[0]
                df_season.columns = ['Date', 'Visitor', 'Goals Visitor', 'Home', 'Goals Home', 'OT', 'Att.', 'LOG', 'Notes']

                del response, html, div

            except Exception as e:
                raise e
        else:
            df_season = pd.DataFrame()

        if playoffs:
            try:
                url = f'https://www.hockey-reference.com/playoffs/NHL_{year}.html'

                response = get(url)
                html = soup(response.text, 'html.parser')

                div = html.find(id="div_all_playoffs")
                tables = div.find_all('tr', class_ = 'toggleable')
                series = [pd.read_html(str(table))[0] for table in tables]

                del response, html, div, tables

                df_playoffs = pd.concat(series, ignore_index=True)
                df_playoffs.columns = ['Game', 'Date', 'Visitor', 'Goals Visitor', 'Home', 'Goals Home', 'OT']
                df_playoffs["Date"] = df_playoffs["Date"].apply(lambda x: f"{year}-{datetime.strptime(x, '%B %d').strftime('%m-%d')}")
                df_playoffs['Notes'] = 'Playoffs'

            except Exception as e:
                raise e
        else:
            df_playoffs = pd.DataFrame()

        df = pd.concat([df_season, df_playoffs], ignore_index=True)

        df = df.convert_dtypes()
        df['Date'] = df['Date'].astype('datetime64')
        df['Notes'][df['Notes'].isnull()] = ''

        return df

    def scrape_elite_prosepcts(self, player):
        ''' FIXME: deprecated
        TODO: use pandas
        '''
        
        url = 'https://www.eliteprospects.com/draft-center/2021#players'
        response = get(url)

        html = soup(response.text, 'html.parser')
        tables = html.find_all('div', class_ = 'table-wizard')

        players = dict()
        data = tables[1].find_all('td')

        # rx = re.compile("\((.+)\)")
        # for row in data:
        #     if row.has_attr('class'):
        #         class_ = row.attrs['class'][0]
        #     else:
        #         continue
            
        #     txt = row.getText().strip()

        #     if class_ == 'player':
        #         pos = rx.search(txt)
        #         if pos is not None:
        #             name = txt[:pos.start()-1]
        #             players[name] = {
        #                 "position" : pos.group()[1:-1],
        #                 "nation" : nation
        #             }
        #         else:
        #             name = ''
        #     elif class_ == 'nation' and len(row.contents) > 1:
        #         flag_id = re.search('\d+', str(row.contents[1])).group()
        #         nation = FLAGS[flag_id]
        #     elif class_ == 'team' and name != '':
        #         players[name]['team'] = txt
        #     elif class_ == 'league' and name != '' :
        #         players[name]['league'] = txt
        #     elif class_ == 'gp' and name != '' :
        #         players[name]['gp'] = txt
        #     elif class_ == 'g' and name != '' :
        #         players[name]['g'] = txt
        #     elif class_ == 'a' and name != '' :
        #         players[name]['a'] = txt
        #     elif class_ == 'tp' and name != '' :
        #         players[name]['tp'] = txt
        #     elif class_ == 'pim' and name != '' :
        #         players[name]['pim'] = txt

        url2 = 'https://www.eliteprospects.com/draft-center/2021?view=info#players'
        response2 = get(url2)

        html = soup(response2.text, 'html.parser')
        tables = html.find_all('div', class_ = 'table-wizard')

        table = tables[1]
        data = table.find_all('td')

        # rx = re.compile("\((.+)\)")
        # for row in data:
        #     if row.has_attr('class'):
        #         class_ = row.attrs['class'][0]
        #     else:
        #         continue
            
        #     txt = row.getText().strip()

        #     if class_ == 'player':
        #         pos = rx.search(txt)
        #         if pos is not None:
        #             name = txt[:pos.start()-1]
        #         else:
        #             name = ''
        #     elif class_ == 'date-of-birth' and name != '':
        #         day, month, year = txt.split('\n')[0].split('/')
        #         players[name]['birth-year'] = year
        #         players[name]['birth-month'] = month
        #     elif class_ == 'height' and name != '' :
        #         players[name]['height'] = txt
        #     elif class_ == 'weight' and name != '' :
        #         players[name]['weight'] = txt
        #     elif class_ == 'shoots' and name != '' :
        #         players[name]['shoots'] = txt

        # pickle.dump(players, open('draft/players.pkl','wb'))

        return NotImplementedError


if __name__ == "__main__":

    scraper = Scraper()

    df = scraper.scrape_scores_by_season(2021, season=True, playoffs=True)