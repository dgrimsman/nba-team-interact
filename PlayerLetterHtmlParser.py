from html.parser import HTMLParser

class PlayerLetterHtmlParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.players = []
        self.state = 'START'

    def handle_starttag(self, tag, attrs):
        if self.state == 'START' and tag == 'table'\
                and ('id', 'players') in attrs:
            self.state = 'IN_TABLE'
        if self.state == 'IN_TABLE' and tag == 'tr':
            self.state = 'FIND_PLAYER'
        if self.state == 'FIND_PLAYER' and tag == 'a':
            self.players.append(attrs[0][1])
            self.state = 'IN_TABLE'

    def handle_endtag(self, tag):
        if self.state == 'IN_TABLE' and tag == 'table':
            self.state = 'DONE'
