'''
.. py:module:: parsing_nltk
    :platform: Unix

Sample code to parse written text to a more appropriate form. This code is
designed to be used to create state transitions for Markov chains.
'''
import os
import re
import nltk
import operator

# Download Alice's Adventures in Wonderland if it is not yet present
alice_file = 'alice.txt'
alice_raw = None

if not os.path.isfile(alice_file):
    from urllib import request
    url = 'http://www.gutenberg.org/cache/epub/19033/pg19033.txt'
    response = request.urlopen(url)
    alice_raw = response.read().decode('utf8')
    with open(alice_file, 'w', encoding='utf8') as f:
        f.write(alice_raw)
else:
    with open(alice_file, 'r', encoding='utf8') as f:
        alice_raw = f.read()

# Remove the start and end bloat from Project Gutenberg (this is not exact, but
# easy).
pattern = r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .+ \*\*\*'
end = "End of the Project Gutenberg"
start_match = re.search(pattern, alice_raw)
if start_match:
    start_index = start_match.span()[1] + 1
else:
    start_index = 0
end_index = alice_raw.rfind(end)
alice = alice_raw[start_index:end_index]
#alice = alice.lower()

# And replace more than one subsequent whitespace chars with one space
alice = re.sub(r'\s+', ' ', alice)

# Tokenize the text into sentences.
sentences = nltk.sent_tokenize(alice)

# Tokenize each sentence to words. Each item in 'words' is a list with
# tokenized words from that list.
tokenized_sentences = []
for s in sentences:
    w = nltk.word_tokenize(s)
    tokenized_sentences.append(w)

# Next, we sanitize the 'words' somewhat. We remove all tokens that do not have
# any Unicode word characters, and force each sentence's last token to '.'.
# You can try other sanitation methods (e.g. look at the last sentence).
is_word = re.compile('\w')
sanitized_sentences = []
for sent in tokenized_sentences:
    sanitized = [token for token in sent if is_word.search(token)] + ['.']
    sanitized_sentences.append(sanitized)

# Now we are ready to create the state transitions. However, this time we
# count the state transitions from each sentence at a time.
#transitions = []
#eachList=['The', 'idea', 'of', 'having', 'the', 'sentence', 'first', '.', 'The', 'idea', 'of', 'having', 'the', 'sentence', 'first']
#eachSentence = ' '.join(e for e in eachList)
#print(eachSentence)
transitions = {}
for eachList in sanitized_sentences:
    #eachSentence = ' '.join(e for e in eachList)
    for i in range(len(eachList)-1):
        pred = eachList[i]
        succ = eachList[i + 1]
        if pred not in transitions:
            # Predecessor key is not yet in the outer dictionary, so we create
            # a new dictionary for it.
            transitions[pred] = {}

        if succ not in transitions[pred]:
            # Successor key is not yet in the inner dictionary, so we start
            # counting from one.
            transitions[pred][succ] = 1.0
        else:
            # Otherwise we just add one to the existing value.
            transitions[pred][succ] += 1.0

#for e in transitions:
#    print(e,':')
#    print(transitions.get(e))

# Compute total number of successors for each state
totals = {}
for pred, succ_counts in transitions.items():
    totals[pred] = sum(succ_counts.values())


# Compute the probability for each successor given the predecessor.
probs = {}
for pred, succ_counts in transitions.items():
    probs[pred] = {}
    for succ, count in succ_counts.items():
        probs[pred][succ] = count / totals[pred]

for e in transitions:
    if e=='Alice':
        sorted_by_values = sorted(probs[e].items(), key=operator.itemgetter(1), reverse=True)
        print(e,sorted_by_values)


# Overall 5 most probable states
words={}
for eachList in sanitized_sentences:
    #print(eachList)
    for i in range(len(eachList) - 1):
        word = eachList[i]
        if word not in words:
            words[word] = {}
            words[word] = 1
        else:
            words[word]+= 1

sorted_by_values = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_by_values[0:100])