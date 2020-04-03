# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:11:17 2020

@author: Cristian
"""
import argparse
import time
import datetime
import re

class Html:
    br = "<br>"
    def div(self, content):
        return "<div>" + content + "</div>"

class Player:
    def __init__(self, nick):
        self.nick = nick
        self.date_last_activity = datetime.datetime.now()

    def inactivity_duration(self):
        return datetime.datetime.now() - self.date_last_activity

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
        return Html().div(self.nick + Html().br + self.display_duration(self.inactivity_duration())+" ago" )

    def __str__(self):
        return self.to_html_string()



# ----------------------------------- File I/O --------------------------------------
def read_text_file(file_name):
    f = open(file_name, "r")
    return f.read()

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
    [part1, part2, part3] = map(read_text_file, ["server_template1.html", "server_template2.html","server_template3.html"])
    
    parser = argparse.ArgumentParser(description='American conquest server message actuator')
    parser.add_argument('fifo_file', help = "input data file to read from")
    parser.add_argument('resulting_file', help = "output html file with data inserted")
    args = parser.parse_args()

    #for info integrity, save and clean fifo
    data = read_text_file(args.fifo_file)
    append_text_to_file(data+"\n","output_archive.txt")
    write_text_to_file("", args.fifo_file)
    

    players = {}
    while True:
        data = read_text_file(args.fifo_file)
        players.update(players)

        if data.strip()!="":
            write_text_to_file("", args.fifo_file) #delete contents after read
            append_text_to_file(data+"\n","output_archive.txt")
            players.update(collect_players(data))

        result = assemble_html(part1, part2, part3, data, players)
        write_text_to_file(result, args.resulting_file)

        time.sleep(5)



# calling
main()
