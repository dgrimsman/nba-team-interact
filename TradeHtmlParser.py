# parses the trade data for the trade pages
from html.parser import HTMLParser

PLAYER_START_STR = '/players/*/'
TEAM_START_STR = '/teams/'

class TradeHtmlParser(HTMLParser):

    def __init__(self, trade_id):
        HTMLParser.__init__(self)
        self.data = {'trade_id': [], 'date': [], 'player': [],
                     'from': [], 'to': []}
        #print('initializing')
        self.trade_id = trade_id
        self.date = ''
        self.state = 'NT'

    def unknown_decl(self, data):
        print('got to unknown')

    def handle_starttag(self, tag, attrs):
        # start of a trade
        # print(attrs)
        if self.state == 'NT' and tag == 'p':
            # print('{} {}'.format(tag, attrs))
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'transaction ':
                    # print('get here')
                    self.state = 'IT'
                    self.trade_id += 1
        # in the table
        elif self.state == 'TB' and tag == 'table':
            self.state = 'PL'

        # player
        elif self.state == 'PL' and tag == 'a':
            ref = attrs[0][1]
            if ref and ref[:8] == PLAYER_START_STR[0:8]:
                name = ref[len(PLAYER_START_STR): -len('.html')]
                self.data['player'].append(name)
                self.data['trade_id'].append(self.trade_id)
                self.data['date'].append(self.date)
                self.state = 'T1'

        # team traded from
        elif self.state == 'T1' and tag == 'a':
            ref = attrs[0][1]
            team = ref[len(TEAM_START_STR): -1]
            self.data['from'].append(team)
            self.state = 'T2'

        #team traded to
        elif self.state == 'T2' and tag == 'a':
            ref = attrs[0][1]
            print(ref)
            team = ref[len(TEAM_START_STR): -1]
            self.data['to'].append(team)
            self.state = 'PL'

    def handle_data(self, d):
        if self.state == 'IT':
            self.date = d
            self.state = 'TB'

    def handle_endtag(self, tag):
        if self.state == 'PL' and tag == 'table':
            self.state = 'NT'
