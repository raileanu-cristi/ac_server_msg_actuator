# about ac_server_msg_actuator
Takes the output of american conquest (cossacks) server updates the information from a webpage stored in the same computer.

# application running
There are 2 methods for starting this application:
1. modify *deploy* file with desired parameters and execute it
1. directly run *src/ac_server_actuator.py* file with desired parameters

# parameters
## required parameters
* **fifo_file**: input data file to read from
* **resulting_main_file**: output html file
* **players_html_file**: output html file for player data
* **lobbies_html_file**: output html file for lobby data

## optional parameters
* **--help**, -h: display help

# application testing
To observe how the application works without running the cossacks server:
1. run the applcation
1. paste some lines from *src/res/ac_server_output_example.txt* into the file indicated by **fifo_file** parameter from time to time
1. watch how the files from **resulting_main_file**, players_html_file and **lobbies_html_file** behave
1. all the lines from fifo file get deleted and appended into *src/data/output_archive.txt*

test

feature/f1 test