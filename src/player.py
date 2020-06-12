from html_simple import  Html
import re
from datetime import datetime
from io_simple import display_duration

class Player:
    dt_format = '%d-%m-%y %H:%M:%S'
    max_inactivity_ignore = 60 # max seconds between 2 activities


    def __init__(self, nick, datetime_str='', duration_play_str=''):
        self.nick = nick
        self.date_last_activity= datetime.now()
        self.duration_of_play = 1
        if datetime_str!='':
            self.date_last_activity = datetime.strptime(datetime_str, Player.dt_format)
        if duration_play_str!='':
            self.duration_of_play = int(duration_play_str)



    def has_valid_nick(self):
        if (re.search("^[a-zA-Z]", self.nick)):
            return True
        else:
            return False



    def inactivity_duration(self):
        return datetime.now() - self.date_last_activity



    def update(self):
        if self.inactivity_duration().seconds <= Player.max_inactivity_ignore:
            self.duration_of_play += self.inactivity_duration().seconds
        self.date_last_activity= datetime.now()
        return self



    def get_xp(self):
        return int(self.duration_of_play / 60)



    def to_html_string(self):
        tags = Html()
        outer_style = "margin-bottom: 4px;border: 1px"
        name_style = "font-size: 20px;"
        return tags.div(tags.div(tags.b(self.nick) , name_style) + tags.div("" + str(self.get_xp()) + "XP" ) + 
               tags.div(display_duration(self.inactivity_duration())+" ago") , outer_style)



    def __str__(self):
        return self.to_html_string()



    def representation(self):
        return self.nick + " " + self.date_last_activity.strftime(self.dt_format) + " " + str(self.duration_of_play)