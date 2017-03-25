# scrape the trade data from basketballreference.com
import urllib.request
from TradeHtmlParser import TradeHtmlParser
import pandas as pd
from sqlalchemy import create_engine

# connect to database
conn_str = 'postgresql://bball:183S!02MkV5hk$KF@127.0.0.1:5432/bball_db'
engine = create_engine(conn_str)
engine.execute("drop table if exists trades;")
query = "create table trades( \
         date varchar(40), \
         from_team varchar(3), \
         player varchar(40), \
         to_team varchar(3), \
         trade_id int, \
         ws_from varchar(5), \
         ws_to varchar(5));"
engine.execute(query)
trade_id = 0
parser = TradeHtmlParser(trade_id)

# list of current teams
curr_teams = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
              'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NJN',
              'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
              'TOR', 'UTA', 'WAS']

done_teams = []
data = pd.DataFrame(columns=['trade_id', 'date', 'player', 'from_team',
                             'ws_from', 'ws_to', 'to_team'])

# iterate through all possible urls
count = 1
for team1 in curr_teams:
    print('scraping trades for {}'.format(team1))
    done_teams.append(team1)
    teams_left = list(set(curr_teams) - set(done_teams))
    for team2 in teams_left:
        # iterate through all trades in the url
        url = 'http://www.basketball-reference.com/friv/trades.fcgi?'
        url += 'f1={}&f2={}'.format(team1, team2)
        page = urllib.request.urlopen(url)
        src = str(page.read())
        parser.feed(src)
        d = pd.DataFrame(parser.data)
        data = data.append(d)
    engine.execute("drop table if exists trades_df")
    data.to_sql('trades_df', engine)
    engine.execute("insert into trades \
                    select date, from_team, player, to_team, trade_id, \
                    ws_from, ws_to \
                    from trades_df;")
engine.execute("drop table trades_df;")
