# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:11:17 2020

@author: Cristian
"""
import argparse
import time
import datetime
import re
import json
from datetime import datetime
import os.path

class Html:
    br = "<br>"
    def div(self, content):
        return "<div>" + content + "</div>"
    def h1(self, content):
        return "<h1>" + content + "</h1>"

class Player:
    dt_format = '%d-%m-%y %H:%M:%S'

    def __init__(self, nick, datetime_str=''):
        self.nick = nick
        self.date_last_activity= datetime.now()

        if datetime_str!='':
            self.date_last_activity = datetime.strptime(datetime_str, Player.dt_format)
            


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
        return Html().div(Html().h1(self.nick) + Html().br + self.display_duration(self.inactivity_duration())+" ago" )

    def __str__(self):
        return self.to_html_string()

    def representation(self):
        return self.nick + " " + self.date_last_activity.strftime(self.dt_format)



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
    names = re.findall("NICK=([^\"]*)", data)
    return dict(map(lambda x: (x, Player(x)), names) )


def assemble_html(part1, part2, part3, data, players):
    lines = get_lines(data)
    return part1+reduce((lambda x,y: x+"\n"+y), map(display_line, lines), "")+part2 + reduce((lambda x,y: x+"\n"+y), map(str, players.values()), "") + part3





def main():
    # constants
    output_archive_file = "output_archive.txt"
    players_file = "players_data"

    [part1, part2, part3] = map(read_text_file, ["server_template1.html", "server_template2.html","server_template3.html"])
    
    #arg parsing
    parser = argparse.ArgumentParser(description='American conquest server message actuator')
    parser.add_argument('fifo_file', help = "input data file to read from")
    parser.add_argument('resulting_file', help = "output html file with data inserted")
    args = parser.parse_args()

    #for info integrity, save and clean fifo
    data = read_text_file(args.fifo_file)
    append_text_to_file(data+"\n", output_archive_file)
    write_text_to_file("", args.fifo_file)
    
    # load players
    players = read_players(players_file)
    #print(players) #debug
    while True:
        data = read_text_file(args.fifo_file)
        players.update(players)

        if data.strip()!="":
            write_text_to_file("", args.fifo_file) #delete contents after read
            append_text_to_file(data+"\n",output_archive_file)
            players.update(collect_players(data))

        result = assemble_html(part1, part2, part3, data, players)
        write_text_to_file(result, args.resulting_file)

        # save players
        write_players(players_file, players)
        time.sleep(5)



# -------------------------------------- calling -------------------------------------------------------------------------------
main()

