# parses the trade data for the trade pages
from html.parser import HTMLParser

PLAYER_START_STR = '/players/*/'
TEAM_START_STR = '/teams/'
WS_COL_NUM = 5

class TradeHtmlParser(HTMLParser):

    def __init__(self, trade_id):
        HTMLParser.__init__(self)
        self.data = {'trade_id': [], 'date': [], 'player': [],
                     'from_team': [], 'ws_from': [], 'to_team': [], 'ws_to': []}
        #print('initializing')
        self.trade_id = trade_id
        self.date = ''
        self.state = 'NT'
        self.col_count = 0

    def unknown_decl(self, data):
        print('got to unknown')

    def rec_ws_from(self, ws='0'):
        self.data['ws_from'].append(ws)
        self.state = 'T2'

    def rec_ws_to(self, ws='0'):
        self.data['ws_to'].append(ws)
        self.state = 'PL'

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
            self.data['from_team'].append(team)
            self.state = 'WS1'
            self.col_count = 0

        # WS for team traded from
        elif self.state == 'WS1' and tag == 'td':
            if self.col_count == WS_COL_NUM:
                self.rec_ws_from()
            self.col_count += 1

        # team traded to
        elif self.state == 'T2' and tag == 'a':
            ref = attrs[0][1]
            # print(ref)
            team = ref[len(TEAM_START_STR): -1]
            self.data['to_team'].append(team)
            self.state = 'WS2'
            self.col_count = 0

        # WS for team traded to
        elif self.state == 'WS2' and tag == 'td':
            if self.col_count == WS_COL_NUM:
                self.rec_ws_to()
            self.col_count += 1

    def handle_data(self, d):
        if self.state == 'IT':
            self.date = d
            self.state = 'TB'
        elif self.state == 'WS1' and self.col_count == WS_COL_NUM:
            if d == '\\n':
                d = '0'
            self.rec_ws_from(ws=d)
        elif self.state == 'WS2' and self.col_count == WS_COL_NUM:
            if d == '\\n':
                d = '0'
            self.rec_ws_to(ws=d)

    def handle_endtag(self, tag):
        if self.state == 'PL' and tag == 'table':
            self.state = 'NT'
