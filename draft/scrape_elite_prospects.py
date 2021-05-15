import re
import pickle
from requests import get
from bs4 import BeautifulSoup

FLAGS = {
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

try:
    response = pickle.load(open('webpage.pkl','rb'))
except:
    # Get Webpage
    url = 'https://www.eliteprospects.com/draft-center/2021#players'
    response = get(url)
    pickle.dump(response, open("webpage.pkl",'wb'))

# Parse data
html = BeautifulSoup(response.text, 'html.parser')
tables = html.find_all('div', class_ = 'table-wizard')

table = tables[1]
data = table.find_all('td')

players = dict()
rx = re.compile("\((.+)\)")
for row in data:
    if row.has_attr('class'):
        class_ = row.attrs['class'][0]
    else:
        continue
    
    txt = row.getText().strip()

    if class_ == 'player':
        pos = rx.search(txt)
        if pos is not None:
            name = txt[:pos.start()-1]
            players[name] = {
                "position" : pos.group()[1:-1],
                "nation" : nation
            }
        else:
            name = ''
    elif class_ == 'nation' and len(row.contents) > 1:
        flag_id = re.search('\d+', str(row.contents[1])).group()
        nation = FLAGS[flag_id]
    elif class_ == 'team' and name != '':
        players[name]['team'] = txt
    elif class_ == 'league' and name != '' :
        players[name]['league'] = txt
    elif class_ == 'gp' and name != '' :
        players[name]['gp'] = txt
    elif class_ == 'g' and name != '' :
        players[name]['g'] = txt
    elif class_ == 'a' and name != '' :
        players[name]['a'] = txt
    elif class_ == 'tp' and name != '' :
        players[name]['tp'] = txt
    elif class_ == 'pim' and name != '' :
        players[name]['pim'] = txt

## Add personal info
try:
    response2 = pickle.load(open('webpage_info.pkl','rb'))
except:
    # Get Webpage
    url2 = 'https://www.eliteprospects.com/draft-center/2021?view=info#players'
    response2 = get(url2)
    pickle.dump(response2, open("webpage_info.pkl",'wb'))

# Parse data
html = BeautifulSoup(response2.text, 'html.parser')
tables = html.find_all('div', class_ = 'table-wizard')

table = tables[1]
data = table.find_all('td')

rx = re.compile("\((.+)\)")
for row in data:
    if row.has_attr('class'):
        class_ = row.attrs['class'][0]
    else:
        continue
    
    txt = row.getText().strip()

    if class_ == 'player':
        pos = rx.search(txt)
        if pos is not None:
            name = txt[:pos.start()-1]
        else:
            name = ''
    elif class_ == 'date-of-birth' and name != '':
        day, month, year = txt.split('\n')[0].split('/')
        players[name]['birth-year'] = year
        players[name]['birth-month'] = month
    elif class_ == 'height' and name != '' :
        players[name]['height'] = txt
    elif class_ == 'weight' and name != '' :
        players[name]['weight'] = txt
    elif class_ == 'shoots' and name != '' :
        players[name]['shoots'] = txt

pickle.dump(players, open('draft/players.pkl','wb'))