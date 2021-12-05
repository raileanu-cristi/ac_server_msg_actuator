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

def display_duration(duration):
    days = duration.days
    seconds = duration.seconds
    hours = duration.seconds / 3600
    minutes = (duration.seconds % 3600) / 60
    if days > 0:
        return str(days)+" days"
    if hours > 0:
        return str(hours) + " hours"
    if minutes > 0:
        return str(minutes) + " minutes"
    return str(seconds) + " seconds"


def display_minutes_hours(seconds):
    hours = seconds / 3600
    minutes = (seconds % 3600) / 60
    if hours > 0:
        return str(hours) + " hours"
    return str(minutes) + " minutes"