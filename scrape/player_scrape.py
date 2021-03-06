import urllib.request
from PlayerLetterHtmlParser import PlayerLetterHtmlParser
from PlayerHtmlParser import PlayerHtmlParser
import pandas as pd
from sqlalchemy import create_engine

# connect to database
conn_str = 'postgresql://bball:183S!02MkV5hk$KF@127.0.0.1:5432/bball_db'
eng = create_engine(conn_str)

# res = eng.execute('select id from players order by id desc limit 1;')
# for row in res:
#    c = row[0][0]
c = 'w'
print('starting at letter ' + c.upper())
base_url = 'http://www.basketball-reference.com'

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letter = letters[0]
while letter != c:
    letters.pop(0)
    letter = letters[0]

for letter in letters:
    team_data = pd.DataFrame(columns=['season', 'player', 'team', 'league',
                                      'ws'])
    player_data = pd.DataFrame(columns=['id', 'name'])
    l_parser = PlayerLetterHtmlParser()
    letter_url = '{}/players/{}/'.format(base_url, letter)
    try:
        page = urllib.request.urlopen(letter_url)
    except urllib.error.HTTPError:
        continue
    src = str(page.read())
    l_parser.feed(src)
    players = l_parser.players
    for player in players:
        pid = player.split('/')[-1][:-5]
        p_parser = PlayerHtmlParser(pid)
        player_url = base_url + player
        page = urllib.request.urlopen(player_url)
        src = str(page.read())
        f = open('tmp.html', 'w')
        f.write(src)
        f.close()
        p_parser.feed(src)
        p_df = pd.DataFrame(p_parser.p_data)
        t_df = pd.DataFrame(p_parser.t_data)
        player_data = player_data.append(p_df)
        team_data = team_data.append(t_df)
    eng.execute('drop table if exists players_df;')
    eng.execute('drop table if exists rosters_df;')
    player_data.to_sql('players_df', eng)
    query = "insert into players \
                 select id, name from players_df;"
    eng.execute(query)
    team_data.to_sql('rosters_df', eng)
    query = "insert into rosters \
             select season, player, team, league, ws from rosters_df;"
    eng.execute(query)
