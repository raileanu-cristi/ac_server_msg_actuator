from datetime import datetime
from html_simple import  Html

class Lobby:
    def __init__(self, name):
        self.name = name
        self.date_last_activity= datetime.now()

    def to_html_string(self):
        tags = Html()
        outer_style = "font-size: 20px;margin-bottom: 4px;border: 1px"
        return tags.div(self.name, outer_style)
    
    def __str__(self):
        return self.to_html_string()

    def inactivity_duration(self):
        return datetime.now() - self.date_last_activity

    def expired(self):
        return self.inactivity_duration().seconds > 300 # 5 minutes