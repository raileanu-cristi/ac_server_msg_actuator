# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:11:17 2020

@author: Cristian
"""

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

def process_line(line):
    return "<div>"+line+"</div>"

def assemble_html(part1, part2, between12):
    lines_between = get_lines(between12)
    return part1+reduce((lambda x,y: x+"\n"+y), map(process_line, lines_between))+part2



def main():
    [part1, part2] = map(read_text_file, ["server_template1.html", "server_template2.html"])
    
    while True:
        between = read_text_file("server_output2.txt")
        write_text_to_file("","server_output2.txt") #delete contents after read
        append_text_to_file(between+"\n","output_archive.txt")
        result = assemble_html(part1, part2, between)
        write_text_to_file(result, "result.html")
    
     
# calling
main()