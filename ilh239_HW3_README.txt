To run my program go into the command line and cd into whatever directory ilh239HW3.py is in. To run type python followed by the training
corpus you are using, followed by your input file(just words), and then the output file which will have the program's output of words and pos
all seperated by spaces. For this viterbi algorithm I used a very simple approach.
I stored the emission and transition probabilities in hash tables. The program
would operate by iterating over a trellis matrix which stored in each column the
probability a certain word would be a certain part of speech. This was found by finding the maximum probability
taking by multiplying the transition probability, emission probability, and pos probability of the previous. Whichever transition, emission and previous pos
combination had the highest probability would be marked as the highest and in the pointer matrix the best previous would be marked.
For words which did not appear in the emission table there would simply be a (1/1000) constant probability.
One problem that I ran into was that after a time the probability got very small and would go to 0 after around a hundred words, so I had to use
logarithms and add them. The best path was found by finding the highest probability at the last word adding whatever that pos was
to the beginning of the bestpath array. It would see what pos was in the pointer matrix and go to that spot in the next column. The process
would repeat until the beginning of the trellis matrix was reached. And best path would have the highest probability list of pos for the corpus.
This was then combined with the words in the input file and put into the output.