from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a {} start tag with attrs {}".format(tag, attrs))

    def handle_endtag(self, tag):
        print("Encountered a {} end tag".format(tag))


page = '<html><h1>Title</h1><p class=\'transcation \'>I\'m a paragraph!</p></html>'

p = MyHTMLParser()
p.feed(page)
