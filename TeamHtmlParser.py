from html.parser import HTMLParser

ABBR_ST = len('/teams/')
ABBR_LEN = 3


class TeamHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.state = 'START'

    def clear(self):
        self.data = {'abbr': [], 'name': [], 'curr': []}
        self.curr = ''

    def handle_starttag(self, tag, attrs):
        if self.state == 'START' and tag == 'table' \
                and ('class', 'sortable stats_table') in attrs:
            self.clear()
            self.state = 'ROW'
        elif self.state == 'ROW' and tag == 'td' \
                and ('data-stat', 'team_name') in attrs:
            self.state = 'ABBR'
        elif self.state == 'ABBR':
            ref = attrs[0][1]
            abbr = ref[ABBR_ST: ABBR_ST + ABBR_LEN]
            if self.curr == '':
                self.curr = abbr
            if abbr not in self.data['abbr']:
                self.data['abbr'].append(abbr)
                self.state = 'NAME'
            else:
                self.state = 'ROW'

    def handle_data(self, d):
        if self.state == 'NAME':
            self.data['name'].append(d)
            self.data['curr'].append(self.curr)
            self.state = 'ROW'

    def handle_endtag(self, tag):
        if tag == 'html':
            self.state = 'START'
