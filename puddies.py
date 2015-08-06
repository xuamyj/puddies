from datetime import datetime
import random

MEMBERS = frozenset(["Director", "Amy", "Armelle", "Charissa", "Dennis", "Kate", "Kyle", "NDAlex", "Allan", "Cindy", "Emily", "Jackie", "James", "John", "Melissa", "Owen"])
HISTORY_FILENAME = 'tmony23.txt'

# returns True if {name1, name2} is valid pair
# prints error messages if error_msg == True
def check_valid(name1, name2, previous, used_names, error_msg):
    if name1 not in MEMBERS or name2 not in MEMBERS:
        if error_msg:
            print 'Error: names not found in members list. '
        return False
    if name1 in used_names or name2 in used_names:
        if error_msg:
            print 'Error: choose people who do not already have puddies. '
        return False
    if name1 == name2:
        if error_msg: 
            print 'Error: a person cannot puddy with themselves. '
        return False
    temp_pair = {name1, name2}
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
        if not line.startswith('#'):
            #strip whitespace from line (otherwise \n becomes part of the name lol)
            line = line.rstrip()
            # generate list of pair strings like 'name1,name2'
            pair_strlist = line.split('|')
            for pair_str in pair_strlist:
                # make each pair a list to add each pair to the set
                pair = pair_str.split(',')
                if len(pair) == 2:
                    previous.add(frozenset([pair[0], pair[1]]))
    f.close()
    return previous

# current and previous are sets of current and previous puddy pairs
# used_names is set of currently used name strings
def custom_generate(current, previous, used_names):
    done = False
    while not done:
        name1 = raw_input('Name of first person in pair? ').strip()
        name2 = raw_input('Name of second person? ').strip()
        if check_valid(name1, name2, previous, used_names, True):
            # add puddy pair
            used_names.add(name1)
            used_names.add(name2)
            current.add(frozenset([name1, name2]))
            print 'Puddy pair added!'
        # done is False if user hits <ENTER> or enters 'y' in response to 'Add another'
        done_check = raw_input('Add another? ')
        done = not (len(done_check) == 0 or done_check.lower().startswith('y'))

# recursive backtracking function that generates puddies
# current: current set of puddies
# previous: set of all previous puddy pairs
# used_names: set of names used in current set of puddies
# unused_names: list of names that need to be puddied
def rec_generate(name1, name2, current, previous, used_names, unused_list):
    # if no names left
    if len(unused_list) == 0:
        return True
    
    # iterate over possible pairs, but in a random order
    random.shuffle(unused_list)
    for i in range(len(unused_list)):
        for j in range(i+1, len(unused_list)):
            new_name1 = unused_list[i]
            new_name2 = unused_list[j]
    
            # if chosen names are not a valid puddy pair
            if not check_valid(new_name1, new_name2, previous, used_names, False):
                continue
            
            # add new pair to storage structures
            used_names.add(new_name1)
            used_names.add(new_name2)
            new_pair = frozenset([new_name1, new_name2])
            current.add(new_pair)
            unused_list.remove(new_name1)
            unused_list.remove(new_name2)

            # recursive step
            if rec_generate(new_name1, new_name2, current, previous, used_names, unused_list):
                return True
            
            # remove new pair
            used_names.remove(new_name1)
            used_names.remove(new_name2)
            current.remove(new_pair)
            unused_list.append(new_name1)
            unused_list.append(new_name2)
    
# wrapper function for puddy generator
def random_generate(current, previous, used_names):
    unused_set = MEMBERS - used_names
    unused_list = list(unused_set)
    if rec_generate('', '', current, previous, used_names, unused_list):
        print 'Puddies generated! '
    else: 
        print 'Error: puddies not generated. '

def display(puddies):
    print
    print 'Puddies: '
    for pair in puddies:
        print ', '.join(str(name) for name in pair)
    print

def save(puddies, filename):
    # create date comment
    date_format = '%A, %b %d'
    date_comment = '# ' + datetime.now().strftime(date_format)
    
    # create puddy string
    puddy_list = []
    for pair in puddies:
        pair_str = ','.join(pair)
        puddy_list.append(pair_str)
    puddy_str = '|'.join(puddy_list)
    
    # add lines to file
    f = open(filename, 'a')
    f.write('\n')
    f.write(date_comment)
    f.write('\n')
    f.write(puddy_str)
    f.close()

if __name__ == '__main__':
    custom_flag = raw_input('Hi there. Custom puddies? ')
    # puddies for this week
    current_puddies = set()
    used_names = set()
    # all previous puddy pairs
    previous_puddies = fetch_previous(HISTORY_FILENAME)
    
    # match custom puddies
    if len(custom_flag) == 0 or custom_flag.lower().startswith('y'):
       custom_generate(current_puddies, previous_puddies, used_names)

    # recursively generate rest of puddies
    print 'Okay, generating puddies. '
    random_generate(current_puddies, previous_puddies, used_names)

    # confirm save
    display(current_puddies)
    save_flag = raw_input('Save? ')
    if len(save_flag) == 0 or save_flag.lower().startswith('y'):
        save(current_puddies, HISTORY_FILENAME)
        print 'Puddies saved! '
    else: 
        print 'Guess not. Okay... bye!'
