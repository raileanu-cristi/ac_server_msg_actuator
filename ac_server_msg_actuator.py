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
from lobby import Lobby
from player import Player
from io_simple import read_text_file, write_text_to_file, append_text_to_file, get_lines, get_words


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
    print("lines= "+lines[0])
    if lines==[]:
        return dict()
    return dict(map(lambda line: (line[0], Player(line[0], line[1]+" "+line[2], line[3])), map(get_words ,lines)))



# ----------------------------------- processing data --------------------------------------



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

# in/out players
def update_players(players, new_players):
    new_guys = dict([ (k, new_players[k]) for k in set(new_players) - set(players) ]) # were not present in players
    old_guys = dict([(k, players[k]) for k in set(new_players) - set(new_guys)])
    players.update(dict(map(lambda x: (x[0], x[1].update()), old_guys.items())))
    players.update(new_guys)
    

# ----------------------------------- app logic --------------------------------------
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
            update_players(players, collect_players(data))
            lobbies.update(collect_lobbies(data))
        
        lobbies = dict(filter(lambda x: not x[1].expired(), lobbies.items()))

        write_text_to_file(assemble_html_players(players), args.players_html_file )
        write_text_to_file(assemble_html_lobbies(lobbies), args.lobbies_html_file )

        # save players
        write_players(players_file, players)
        time.sleep(5)



# -------------------------------------- calling -------------------------------------------------------------------------------
main()

