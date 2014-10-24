from datetime import datetime

MEMBERS = frozenset(["Director", "Amy", "Armelle", "Charissa", "Dennis", "Kate", "Kyle", "NDAlex", "Allan", "Cindy", "Emily", "Jackie", "James", "John", "Melissa", "Owen"])
HISTORY_FILENAME = 'test.txt'

# returns True if {name1, name2} is valid pair
# prints error messages if error_msg == True
def check_valid(name1, name2, current, previous, error_msg):
    if name1 not in MEMBERS or name2 not in MEMBERS:
        if error_msg:
            print 'Error: names not found in members list. '
        return False
    if name1 == name2:
        if error_msg: 
            print 'Error: a person cannot puddy with themselves. '
        return False
    temp_pair = {name1, name2}
    if temp_pair in current:
        if error_msg:
            print 'Error: this is already a puddy pair for this week. '
        return False
    if temp_pair in previous:
        if error_msg:
            print 'Error: these people have already puddied. '
        return False
    return True

# returns set of all previous puddy pairs
# assume file is formatted correctly
def fetch_previous(filename):
    previous = set()
    f = open(filename)
    for line in f:
        # line is not a comment
        if len(line) > 0 and line[0] != '#':
            # generate list of pair strings like 'name1,name2'
            pair_strlist = line.split('|')
            for pair_str in pair_strlist:
                # make each pair a list to add each pair to the set
                pair = pair_str.split(',')
                previous.add({pair[0], pair[1]})
    f.close()
    return previous

def custom_generate(current, previous):
    done = False
    while not done:
        name1 = raw_input('Name of first person in pair? ')
        name2 = raw_input('Name of second person? ')
        if checkvalid(name1, name2, current, previous, True):
            current.add({name1, name2})
            print 'Puddy pair added!'
        # done is False if user enters 'y' in response to 'Add another'
        done_check = raw_input('Add another? ')
        done = len(done_check) > 0 and done_check[0].lower() != 'y'

# recursive backtracking function that generates puddies
# def rec_generate(puddies, used...):

# wrapper function for puddy generator
def random_generate(puddies, used):
    return

def display(puddies):
    print 
    for pair in puddies:
        print ', '.join(puddies)
    print

def save(puddies, filename):
    # create date comment
    date_format = '%a, %b %d'
    date_comment = '# ' + datetime.strftime(date_format)
    
    # create puddy string
    puddy_list = []
    for pair in puddies:
        pair_str = ','.join(pair)
        puddy_list.append(pair_str)
    puddy_str = '|'.join(puddy_list)
    
    # add lines to file
    f = open(filename, 'a')
    f.write(date_comment)
    f.write(puddy_str)
    f.close()

if __name__ == '__main__':
    custom_flag = raw_input('Hi there. Custom puddies? ')
    # puddies for this week
    current_puddies = set()
    # all previous puddy pairs
    previous_puddies = fetch_previous(HISTORY_FILENAME)
    
    # match custom puddies
    if (len(custom_flag) == 0 or custom_flag[0].lower() == 'y'):
       custom_generate(current_puddies, previous_puddies)

    # recursively generate rest of puddies
    print 'Okay, generating puddies. '
    random_generate(current_puddies, previous_puddies)

    # confirm save
    display(current_puddies)
    save_flag = raw_input('Save? ')
    if (len(save_flag) == 0 or save_flag[0].lower() == 'y'):
        save(current_puddies, HISTORY_FILENAME)
        print 'Puddies saved! '
    else: 
        print 'Guess not? Okay... bye!'
