from pathlib import Path
import operator

# creates
emissiontable = {}
transitiontable = {}


# for everyline it updates the values of the emission table
def line(a_line, table):
    # splits the line into both pos and word
    values = a_line.split()
    word = values[0]
    pos = values[1]

    # if word is in the dictionary will go into part of speech
    if word in table.keys():
        # if pos is in the dictionary then it will add 1 value to the table
        if pos in table[word].keys():
            table[word][pos] += 1
        else:
            # else it will create the key with a value of 1
            table[word][pos] = 1
    # else it will create the dictionary for that word
    # it will also create a dictionary for the part of speech with the total starting at 1
    else:
        table[word] = {}
        table[word][pos] = 1


# format table[word][pos] this given the word and pos is probability that a certain word is

def line2(pos, previous, table):
    # checks if previous is in the table
    if previous in table.keys():
        # checks if it's in the previous dict
        if pos in table[previous].keys():
            # if both are true it will add 1 to the value
            table[previous][pos] += 1
        else:
            # else it will create a dict within previous
            table[previous][pos] = 1
    else:
        # will create the previous key with pos key inside and have it start at value 1
        table[previous] = {}
        table[previous][pos] = 1


# the format for finding a proability emissiontable[previous part of speech][next part of speech] percent chance that previous pos leads to next

# method for creating the emission probability table
def emission(file, table):
    a_file = open(file, 'r')
    lines = a_file.readlines()
    for a_line in lines:
        # if a_line is just a space it will skip it
        if a_line.isspace():
            continue
        else:
            line(a_line, emissiontable)
    probability(table)


# method to turn pos values into probabilities
def probability(dict):
    # loops through the dictionary and finds the values
    for i in dict:
        # finds the total value of all instances of the word
        values = dict[i].values()
        total = sum(values)
        for j in dict[i]:
            # divides the pos by the total number of instances to get probability
            dict[i][j] = dict[i][j] / total


# creates the transition probabilities
def transition(file, table):
    # opens the file
    a_file = open(file, 'r')
    # converts into list of strings
    lines = a_file.readlines()
    # sets previous pos to "." Period will signify the beginning and the end of a sentence
    previous = "."
    # iterates through the list of lines
    for a_line in lines:
        # if the line is blank then it skips the line
        if a_line.isspace():
            continue
        else:
            # extracts the pos from the line
            values = a_line.split()
            pos = values[1]
            # calls upon the method function to insert the pos into the table
            line2(pos, previous, table)
            previous = pos
    probability(table)


# so we now have the transition and probability tables
# now we must make the viterbi algorithm
def viterbi(inputfile, etable, ttable, output):
    file = open(inputfile, 'r')
    lines = file.readlines()
    previous = "."
    # iterates through the list
    number = 0
    for line in lines:
        # creates a dictionary called values
        values = {}
        for i in etable[line]:
            # multiplies the emission probability with the corresponding transition probability
            x = {i: (etable[line][i] * ttable[previous][i])}
            # adds the value to dict values, the key is the part of speech
            values.update(x)
        # this adds the max value of the list to the output in the list it will be a part of speech
        output[number] = values[max(values, key=values.get)]
        previous = line
        number += 1


emission("WSJ_02-21.pos", emissiontable)
transition("WSJ_02-21.pos", transitiontable)
print(transitiontable.values())
print(transitiontable.keys())
