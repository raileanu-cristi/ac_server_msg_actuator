# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:11:17 2020

@author: Cristian
"""
import argparse
import time
import datetime
from datetime import datetime
import re
import os.path

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

# ------------------------------------- Player ------------------------------------------------
class Player:
    dt_format = '%d-%m-%y %H:%M:%S'

    def __init__(self, nick, datetime_str=''):
        self.nick = nick
        self.date_last_activity= datetime.now()

        if datetime_str!='':
            self.date_last_activity = datetime.strptime(datetime_str, Player.dt_format)
            
    def has_valid_nick(self):
        if (re.search("^[a-zA-Z]", self.nick)):
            return True
        else:
            return False

    def inactivity_duration(self):
        return datetime.now() - self.date_last_activity

    def display_duration(self, duration):
        days = duration.days
        seconds = duration.seconds
        hours = duration.seconds / 3600
        minutes = (duration.seconds % 3600) / 60
        seconds = duration.seconds
        if days > 0:
            return str(days)+" days"
        if hours > 0:
            return str(hours) + " hours"
        if minutes > 0:
            return str(minutes) + " minutes"
        
        return str(seconds) + " seconds"

    def to_html_string(self):
        tags = Html()
        outer_style = "margin-bottom: 4px;border: 1px"
        name_style = "font-size: 20px;"
        return tags.div(tags.div(tags.b(self.nick) , name_style) + tags.div(self.display_duration(self.inactivity_duration())+" ago"), outer_style)

    def __str__(self):
        return self.to_html_string()

    def representation(self):
        return self.nick + " " + self.date_last_activity.strftime(self.dt_format)
# --------------- end Player ------------------------------------------------------------------------------

# ------------------------------------- Lobby ------------------------------------------------
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
# --------------- end Lobby ------------------------------------------------------------------------------

# ----------------------------------- File I/O --------------------------------------
def read_text_file(file_name):
    f = open(file_name, "r")
    s = f.read()
    f.close()
    return s

def write_text_to_file(text, file_name):
    f= open(file_name,"w")
    f.write(text)
    f.close()

def append_text_to_file(text, file_name):
    f= open(file_name,"a")
    f.write(text)
    f.close()

def get_lines(text):
    return text.split('\n')

def get_words(text):
    return text.split(' ')


# ////////////////////////////////////////    write ///////////////////////////////////////////////////////////////
#
def write_players(file_name, players):
    dfile = open(file_name, "w")
    map(dfile.write, map(lambda x: x.representation()+"\n" ,players.values()))
    dfile.close()
    return

# ////////////////////////////////////////    read ///////////////////////////////////////////////////////////////
#
def read_players(file_name):
    s=''
    if os.path.isfile(file_name):
        f = open(file_name, "r")
        s = f.read()
        f.close()
    lines = filter(lambda x:x!='', map(lambda x:x.strip(), get_lines(s)))
    #print(lines)
    if lines==[]:
        return dict()
    return dict(map(lambda line: (line[0], Player(line[0], line[1]+" "+line[2])), map(get_words ,lines)))



# ----------------------------------- processing data --------------------------------------
def display_line(line):
    return Html().div(line)


def collect_players(data):
    # names = re.findall("NICK=([^\"]*)", data)
    names = re.findall("[.][\d]+[.][\d]+\s([a-zA-Z][^:]+)", data)
    return dict(map(lambda x: (x, Player(x)), names) )


def collect_lobbies(data):
    names = re.findall("VE_TITLE=([^\^]*)", data)
    return dict(map(lambda x: (x, Lobby(x)), names))


def assemble_html_players(data_dict):
    return reduce((lambda x,y: x+"\n"+y), map(str, sorted(data_dict.values(), reverse=True, key=lambda x:x.date_last_activity) ), "")

def assemble_html_lobbies(data_dict):
    return reduce((lambda x,y: x+"\n"+y), map(str, data_dict.values() ), "")

def filter_players(players):
    return dict(filter(lambda x: x[1].has_valid_nick(), players.items()))

def main():
    # constants
    output_archive_file = "output_archive.txt"
    players_file = "players_data"
    server_html_file = "server.html"
    
    #arg parsing
    parser = argparse.ArgumentParser(description='American conquest server message actuator')
    parser.add_argument('fifo_file', help = "input data file to read from")
    parser.add_argument('resulting_main_file', help = "output html file")
    parser.add_argument('players_html_file', help = "output html file for player data")
    parser.add_argument('lobbies_html_file', help = "output html file for lobby data")
    args = parser.parse_args()

    #for info integrity, save and clean fifo
    data = read_text_file(args.fifo_file)
    append_text_to_file(data+"\n", output_archive_file)
    write_text_to_file("", args.fifo_file)
    
    write_text_to_file(read_text_file(server_html_file), args.resulting_main_file)

    # load players
    players = filter_players(read_players(players_file))
    lobbies = {}
    while True:
        data = read_text_file(args.fifo_file)

        if data.strip()!="":
            write_text_to_file("", args.fifo_file) #delete contents after read
            append_text_to_file(data+"\n",output_archive_file)
            players.update(collect_players(data))
            lobbies.update(collect_lobbies(data))
        
        lobbies = dict(filter(lambda x: not x[1].expired(), lobbies.items()))

        write_text_to_file(assemble_html_players(players), args.players_html_file )
        write_text_to_file(assemble_html_lobbies(lobbies), args.lobbies_html_file )

        # save players
        write_players(players_file, players)
        time.sleep(5)



# -------------------------------------- calling -------------------------------------------------------------------------------
main()

