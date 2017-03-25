from html.parser import HTMLParser


class PlayerCommentHtmlParser(HTMLParser):
    
    def __init__(self, pid):
        HTMLParser.__init__(self)
        self.state = 'TABLE'
        self.t_data = {'season': [], 'player': [], 'team': [], 'league': [],
                       'ws': []}
        self.pid = pid
        self.found_data = False
    
    def handle_starttag(self, tag, attrs):
        if self.state == 'TABLE' and tag == 'table' \
                and ('id', 'advanced') in attrs:
            self.found_data = True
            self.state = 'FIRST_ROW'

        elif self.state == 'FIRST_ROW' and tag == 'tr':
            self.state = 'ROW'

        elif self.state == 'ROW' and tag == 'tr':
            self.state = 'SEASON'

        elif self.state == 'FIND_WS' and tag == 'td' and \
                ('data-stat', 'ws') in attrs:
            self.state = 'WS'
     
    def handle_data(self, d):
        if self.state == 'SEASON':
            if d == 'Career':
                self.state = 'DONE'
            else:
                self.t_data['season'].append(d)
                self.t_data['player'].append(self.pid)
                self.state = 'AGE'

        elif self.state == 'AGE':
            self.state = 'TEAM'

        elif self.state == 'TEAM':
            if d == 'TOT':
                self.t_data['season'].pop()
                self.t_data['player'].pop()
                self.state = 'ROW'
            else:
                self.t_data['team'].append(d)
                self.state = 'LEAGUE'

        elif self.state == 'LEAGUE':
            self.t_data['league'].append(d)
            self.state = 'FIND_WS'

        elif self.state == 'WS':
            self.t_data['ws'].append(d)
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