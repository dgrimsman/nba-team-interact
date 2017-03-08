from html.parser import HTMLParser


class PlayerHtmlParser(HTMLParser):

    def __init__(self, pid):
        HTMLParser.__init__(self)
        self.pid = pid
        self.state = 'START'
        self.t_data = {'season': [], 'player': [], 'team': [], 'league': []}
        self.p_data = {'id': [pid]}

    def handle_starttag(self, tag, attrs):
        if self.state == 'START' and tag == 'div' \
                and ('itemtype', 'http://schema.org/Person') in attrs:
            self.state = 'HEADER'

        elif self.state == 'HEADER' and tag == 'h1':
            self.state = 'NAME'

        elif self.state == 'TABLE' and tag == 'table' \
                and ('id', 'per_game') in attrs:
            self.state = 'FIRST_ROW'

        elif self.state == 'FIRST_ROW' and tag == 'tr':
            self.state = 'ROW'

        elif self.state == 'ROW' and tag == 'tr':
            self.state = 'SEASON'

    def handle_data(self, d):
        if self.state == 'NAME':
            self.p_data['name'] = [d]
            print('player name: ' + d)
            self.state = 'TABLE'

        elif self.state == 'SEASON':
            if d == 'Career':
                self.state = 'DONE'
            else:
                self.t_data['season'].append(d)
                self.t_data['player'].append(self.pid)
                self.state = 'AGE'

        elif self.state == 'AGE':
            self.state = 'TEAM'

        elif self.state == 'TEAM':
            self.t_data['team'].append(d)
            self.state = 'LEAGUE'

        elif self.state == 'LEAGUE':
            self.t_data['league'].append(d)
            self.state = 'ROW'

    def handle_endtag(self, tag):
        if self.state == 'ROW' and tag == 'table':
            self.state = 'DONE'

        elif self.state == 'SEASON' and tag == 'tr':
            self.state = 'ROW'

        elif self.state in ['AGE', 'TEAM'] and tag == 'tr':
            self.t_data['season'].pop()
            self.t_data['player'].pop()
            self.state = 'ROW'

        elif self.state == 'LEAGUE' and tag == 'tr':
            self.t_data['season'].pop()
            self.t_data['player'].pop()
            self.t_data['team'].pop()
            self.state = 'ROW'
