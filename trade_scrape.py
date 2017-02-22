# scrape the trade data from basketballreference.com
import urllib.request
from TradeHtmlParser import TradeHtmlParser
import pandas as pd
from sqlalchemy import create_engine

# connect to database
engine = create_engine('postgresql://bball:183S!02MkV5hk$KF@127.0.0.1:5432/bball_db')
query = 'drop table if exists trades_df'
engine.execute(query)
trade_id = 0
parser = TradeHtmlParser(trade_id)

# list of current teams
curr_teams = ['ATL', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
              'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NJN',
              'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS',
              'TOR', 'UTA', 'WAS']

done_teams = []
data = pd.DataFrame(columns=['trade_id', 'date', 'player', 'from', 'ws_from',
                             'ws_to', 'to'])

# iterate through all possible urls
for team1 in curr_teams:
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
        break
    data.to_sql('trades_df', engine)
    break

print(parser.data)
