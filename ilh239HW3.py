import math
from pathlib import Path
import operator
import numpy as np
import sys

# creates
from sys import maxsize

emissiontable = {}
transitiontable = {}
developmentcorpus = sys.argv[1]
testcorpus = sys.argv[2]
outputfile = sys.argv[3]

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
        # if a_line is just a space will stick it into the emission table with a word of space and pos of space
        if a_line.isspace():
            line("space space", emissiontable)
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
        # if the line is blank then we treat the pos as space
        if a_line.isspace():
            line2("space", previous, table)
            previous = "space"
        else:
            # extracts the pos from the line
            values = a_line.split()
            pos = values[1]
            # calls upon the method function to insert the pos into the table
            line2(pos, previous, table)
            previous = pos
    probability(table)


def states(trtable):
    states = []
    for i in trtable.keys():
        states.append(i)
    return states


# this method makes sure that every single "key" word in the emission table and pos in the transition table has pos as 0. Because other-
# wise they would not exist
def makesure(trtable, emtable, states):
    for i in trtable:
        for x in states:
            if x not in trtable[i]:
                #   these are the smallest numbers possible
                trtable[i][x] = np.nextafter(0, 1)
            else:
                continue
    for a in emtable:
        for c in states:
            if c not in emtable[a]:
                emtable[a][c] = np.nextafter(0, 1)
            else:
                continue


def convertinput(inputfile):
    file = open(inputfile, 'r')
    lines = file.readlines()
    obs = []
    i = 0
    for line in lines:
        if line.isspace():
            obs.append("actualspace")
        else:
            line2 = line.split()
            # converts to string
            str1 = ' '.join(line2)
            obs.append(str1)
        i += 1
    return obs



def convertoutput(outputfile, obs, states):
    with open(outputfile, 'w') as f:
        j = 0
        for i in obs:
            # if it's a space we will always put down a space so there are no format issues
            if i == "actualspace":
                f.write("")
                f.write("\n")
            # if viterbi incorrectly labeled it as a space it will simply put down space for the part of speech
            else:
                f.write(i + "\t" + states[j])
                f.write("\n")
            j += 1
def special_log(f):
    if(f == 0.0):
        return -1.0e300
    else:
        return math.log(f)

def viterbi(obs, states, emtable, trtable):
    # Trellis Matrix
    # Log Trellis Matrix
    # trellis is the log of probabilities
    # so if smallval is in there it means the probability is 1.0e(-1.0e300)
    # this is much smaller that the log of the smallest number representable
    # log(1.0e-300 ) = -300 so we are using -300000000000000000000000000000000000000000000000000
    smallval = -1.0e300
    trellis = [[smallval for i in range(len(states))] for j in range(len(obs))]
    # sets the first word's part of speech probability
    i = 0
    for st in states:
        # sets the first probabilities in the trellis
        if obs[0] not in emtable:
            trellis[0][i] = math.log(1 / 1000) + math.log(trtable["space"][st])
        else:
            trellis[0][i] = math.log(emtable[obs[0]][st]) + math.log(trtable["space"][st])
        i += 1
    # Pointer Matrix
    pointer = [[0 for i in range(len(states))] for j in range(len(obs))]


    # iterates through the words (the, dog, ran)
    a = 1
    # we start at the second word because the first word in the trellis has already been set up
    for ob in obs[1:]:
        b = 0
        # iterates through the current column/states
        # max_in_column is the log of a probability.
        max_in_column = smallval

        for st in states:
            c = 0

            # finds the maximum probability for the current state by iterating through the previous states
            for stprev in states:
                # this branch is utilized if the word is out of vocabulary then we will multiply by constant
                if ob not in emtable:
                    # if the probability of the previous state multiplied by emission and transition is greater it
                    # becomes maximum
                    if trellis[a - 1][c] + math.log(trtable[stprev][st]) + math.log(1 / 1000) > trellis[a][b]:
                        trellis[a][b] = trellis[a - 1][c] + math.log(trtable[stprev][st]) + math.log(1 / 1000)
                        # sets the word to point the maximum previous word
                        pointer[a][b] = stprev
                elif trellis[a - 1][c] + math.log(trtable[stprev][st]) + math.log(emtable[ob][st]) > trellis[a][b]:
                    # if the probability of the previous state multiplied by emission and transition is greater it
                    # becomes maximum
                    trellis[a][b] = trellis[a - 1][c] + math.log(trtable[stprev][st]) + math.log(emtable[ob][st])
                    # sets the word to point the maximum previous word
                    pointer[a][b] = stprev
                c += 1
# trellis[a][b] should now be set
                if(trellis[a][b] > max_in_column):
                    max_in_column = trellis[a][b]
            b += 1
        # at this point we have process the word "ob" at position a.


        a += 1

    # Now we will go through the pointer Matrix to find the greatest path
    # first we must find the greatest last probability
    # sets the max to 0
    # iterates through the last columns in the trellis matrix
    # so it seems that our trellis matrix is correct.
    maxindex = 0
    max = smallval
    a = 0
    # finds the maximum of the last column in the trellis


    for f in trellis[-1]:
        if f > max:
            max = f
            maxindex = a
        a += 1
    # creates the best path
    bestpath = []

    # reverse goes through the matrix
    last_trellis = trellis[-1]
    a = 0
    states.append(0)
    for i in reversed(pointer):
        # adds whatever the current state is at the beginning of the bestpath array
        bestpath.insert(0, states[maxindex])
        # sets maxindex to wherever the previous pos pointed to
        maxindex = states.index(i[maxindex])
    states.remove(0)

    return bestpath


emission(developmentcorpus, emissiontable)
transition(developmentcorpus, transitiontable)
states = states(transitiontable)
makesure(transitiontable, emissiontable, states)
input_1 = convertinput(testcorpus)
bestoutput = viterbi(input_1, states, emissiontable, transitiontable)
convertoutput(outputfile, input_1, bestoutput)
