import urllib.request
from PlayerLetterHtmlParser import PlayerLetterHtmlParser
from PlayerHtmlParser import PlayerHtmlParser
import pandas as pd
from sqlalchemy import create_engine

# connect to database
conn_str = 'postgresql://bball:183S!02MkV5hk$KF@127.0.0.1:5432/bball_db'
eng = create_engine(conn_str)
eng.execute("drop table if exists rosters;")
query = "create table roster ( \
         season varchar(9), \
         player varchar(40), \
         team varchar(3), \
         league varchar(5));"
eng.execute(query)
eng.execute("drop table if exists players;")
query = "create table players ( \
         id varchar(40), \
         name varchar(50));"
eng.execute(query)

base_url = 'http://www.basketball-reference.com'

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

l_parser = PlayerLetterHtmlParser()
p_parser = PlayerHtmlParser()
team_data = pd.DataFrame(columns=['season', 'player', 'team', 'league'])
player_data = pd.DataFrame(columns=['id', 'name'])
for letter in letters:
    letter_url = '{}/players/{}/'.format(base_url, letter)
    page = urllib.request.urlopen(letter_url)
    src = str(page.read())
    l_parser.feed(src)
    players = l_parser.players
    for player in players:
        player_url = base_url + player
        page = urllib.request.urlopen(player_url)
        src = str(page.read())
        p_parser.feed(src)
        p_df = pd.DataFrame(p_parser.p_data)
        t_df = pd.DataFrame(p_parser.t_data)
        player_data = player_data.append(p_df)
        team_data = team_data.append(t_df)
    player_data.to_sql('players_df', eng)
    query = "insert into players \
                 select id, name from players_df;"
    eng.execute(query)
    team_data.to_sql('rosters_df', eng)
    query = "insert into rosters \
             select season, player, team, league from rosters_df;"
    eng.execute(query)
