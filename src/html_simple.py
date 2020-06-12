class Html:
    br = "<br>"
    def div(self, content, style=''):
        if style!='':
            return "<div style=\"" + style + "\">" + content + "</div>"
        return "<div>" + content + "</div>"
    def h3(self, content):
        return "<h3>" + content + "</h3>"
    def b(self, content):
        return "<b>" + content + "</b>"

def display_line(line):
    return Html().div(line)