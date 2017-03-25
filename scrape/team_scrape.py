# scrape the team data from basketballreference.com
import urllib.request
from TeamHtmlParser import TeamHtmlParser
import pandas as pd
from sqlalchemy import create_engine

# connect to database
conn_str = 'postgresql://bball:183S!02MkV5hk$KF@127.0.0.1:5432/bball_db'
eng = create_engine(conn_str)
eng.execute("drop table if exists teams;")
# query = "create table teams( \
#         abbr varchar (3), \
#         name varchar (40), \
#         curr varchar(3));"
# eng.execute(query)

curr_teams = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
              'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NJN',
              'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
              'TOR', 'UTA', 'WAS']

parser = TeamHtmlParser()
url_base = 'http://www.basketball-reference.com/teams/'
data = pd.DataFrame(columns=['abbr', 'name', 'curr'])
for team in curr_teams:
    print('gathering all names for ' + team)
    page = urllib.request.urlopen(url_base + team)
    src = str(page.read())
    parser.feed(src)
    d = pd.DataFrame(parser.data)
    data = data.append(d)

data.to_sql('teams', eng)
