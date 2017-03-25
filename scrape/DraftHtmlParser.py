# parses the draft data for the draft pages
from html.parser import HTMLParser

class DraftHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {'year':[], 'team':[], 'player':[]}
        self.year = 2018
        self.state = 'START'

    def set_year(self, year):
        self.year = year

    def handle_starttag(self, tag, attrs):

        if self.state == 'START' and tag == 'table' \
                and ('id', 'stats') in attrs:
            self.data = {'year':[], 'team':[], 'player':[]}
            self.state = 'ROW'

        elif self.state == 'ROW' and tag == 'td' \
                and ('data-stat', 'team_id') in attrs:
            self.state = 'TEAM'

        elif self.state == 'TEAM' and tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    ref = attr[1]
                    break
            team = ref[7:10]
            self.data['year'].append(self.year)
            self.data['team'].append(team)
            self.state = 'PLAYER'

        elif self.state == 'PLAYER' and tag == 'td' \
                and ('data-stat', 'player') in attrs:
            has_link = False
            for attr in attrs:
                if attr[0] == 'data-append-csv':
                    has_link = True
                    break
            if has_link:
                self.data['player'].append(attr[1])
            else:
                self.data['year'].pop()
                self.data['team'].pop()
            self.state = 'ROW'

    def handle_endtag(self, tag):
        if self.state == 'PLAYER' and tag == 'tr':
            self.data['team'].pop()
            self.data['year'].pop()
            self.row_num += 1
            self.state = 'ROW'
        elif self.state in ['ROW', 'TEAM', 'PLAYER'] and tag == 'table':
            self.state = 'START'
