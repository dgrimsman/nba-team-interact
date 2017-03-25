from html.parser import HTMLParser
from PlayerCommentHtmlParser import PlayerCommentHtmlParser


class PlayerHtmlParser(HTMLParser):

    def __init__(self, pid):
        HTMLParser.__init__(self)
        self.pid = pid
        self.state = 'START'
        self.p_data = {'id': [pid]}

    def handle_starttag(self, tag, attrs):
        if self.state == 'START' and tag == 'div' \
                and ('itemtype', 'http://schema.org/Person') in attrs:
            self.state = 'HEADER'

        elif self.state == 'HEADER' and tag == 'h1':
            self.state = 'NAME'

    def handle_data(self, d):
        if self.state == 'NAME':
            self.p_data['name'] = [d]
            print('player name: ' + d)
            self.state = 'TABLE'

    def handle_comment(self, d):
        if self.state == 'TABLE':
            parser = PlayerCommentHtmlParser(self.pid)
            parser.feed(d)
            if parser.found_data:
                self.t_data = parser.t_data
                self.state = 'DONE'
