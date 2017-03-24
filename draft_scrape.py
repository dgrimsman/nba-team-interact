# scrape draft data
import urllib.request
from DraftHtmlParser import DraftHtmlParser
from sqlalchemy import create_engine
import pandas as pd

# connect to database
conn_str = 'postgresql://bball:183S!02MkV5hk$KF@127.0.0.1:5432/bball_db'
eng = create_engine(conn_str)
eng.execute("drop table if exists drafts;")
query = "create table drafts( \
         year varchar(4), \
         team varchar(3), \
         player varchar(40));"
eng.execute(query)
years = range(1947, 2017)
parser = DraftHtmlParser()

for year in years:
    print('scraping draft for {}'.format(year))
    data = pd.DataFrame(columns=['year', 'team', 'player'])
    parser.set_year(year)
    url = 'http://www.basketball-reference.com/draft/'
    if year < 1950:
        url += 'BAA'
    else:
        url += 'NBA'
    url += '_' + str(year) + '.html'
    page = urllib.request.urlopen(url)
    src = str(page.read())
    parser.feed(src)
    d = pd.DataFrame(parser.data)
    data = data.append(d)
    eng.execute('drop table if exists drafts_df;')
    data.to_sql('drafts_df', eng)
    eng.execute('insert into drafts \
                 select year, team, player \
                 from drafts_df;')
    
eng.execute('drop table drafts_df;')
