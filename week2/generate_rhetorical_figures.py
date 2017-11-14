import re
import nltk
import random
import os
from collections import Counter

# Download Alice's Adventures in Wonderland if it is not yet present
def read_alice_in_wonderland():
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

    # Remove the start and end bloat from Project Gutenberg (this is not exact, but easy).
    pattern = r'\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .+ \*\*\*'
    end = "End of the Project Gutenberg"
    start_match = re.search(pattern, alice_raw)
    if start_match:
        start_index = start_match.span()[1] + 1
    else:
        start_index = 0
    end_index = alice_raw.rfind(end)
    alice = alice_raw[start_index:end_index]

    # And replace more than one subsequent whitespace chars with one space
    raw_text = re.sub(r'\s+', ' ', alice)
    return raw_text

# Use any order markov chain model
def markov_chain(raw_text, order=1):
    # Tokenize the text into sentences.
    sentences = nltk.sent_tokenize(raw_text)

    # Tokenize each sentence to words. Each item in 'words' is a list with
    # tokenized words from that list.
    tokenized_sentences = []
    for s in sentences:
        singleWordTokens = nltk.word_tokenize(s)
        tokenized_sentence = []
        for i in range(0, len(singleWordTokens) - order + 1):
            counter = 0
            stateElements = []
            for j in range(i, i + order):
                # print(w[j])
                stateElements.append(singleWordTokens[j])
            orderSizeState = ' '.join(stateElements)
            tokenized_sentence.append(orderSizeState)
        tokenized_sentences.append(tokenized_sentence)

    print('States from text:', tokenized_sentences)

    transitions = {}
    for eachList in tokenized_sentences:
        for i in range(len(eachList) - 1):
            pred = eachList[i]
            succ = eachList[i + 1].split()[order - 1]
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

    totals = {}
    for pred, succ_counts in transitions.items():
        totals[pred] = sum(succ_counts.values())

    # Compute the probability for each successor given the predecessor.
    probs = {}
    for pred, succ_counts in transitions.items():
        probs[pred] = {}
        for succ, count in succ_counts.items():
            probs[pred][succ] = count / totals[pred]

    return probs

# make cdfs
def make_cdfs_from_probs(probabilities_dict):
    import operator
    cdfs = {}
    for pred, succ_probs in probabilities_dict.items():
        items = succ_probs.items()
        # Sort the list by the second index in each item and reverse it from
        # highest to lowest.
        sorted_items = sorted(items, key=operator.itemgetter(1), reverse=True)
        cdf = []
        cumulative_sum = 0.0
        for c, prob in sorted_items:
            cumulative_sum += prob
            cdf.append([c, cumulative_sum])
        cdf[-1][1] = 1.0 # For possible rounding errors
        cdfs[pred] = cdf
    return cdfs

def generate_2(state_transition_probabilities_1, state_transition_probabilities_2,length=10, start=None):
    if (start == None):
        start = random.choice(list(state_transition_probabilities_2.keys()))

    cdfs_1 = make_cdfs_from_probs(state_transition_probabilities_1)
    cdfs_2 = make_cdfs_from_probs(state_transition_probabilities_2)

    markov_chain = [start]
    i = 0
    while len(markov_chain) < length and markov_chain[len(markov_chain) - 1] != '.':
        lastState = markov_chain[len(markov_chain) - 1]
        wordsInLastState = lastState.split()
        if (len(wordsInLastState) < 2):
            if (len(markov_chain) > 1):
                # print('Join 2 states:')
                secondLastState = markov_chain[len(markov_chain) - 2]
                wordsInSecondLastState = secondLastState.split()
                if (len(wordsInSecondLastState) > 0):
                    fromPrev = wordsInSecondLastState[len(wordsInSecondLastState) - 1]
                    lastState = fromPrev + ' ' + lastState

        pred = lastState
        rnd = random.random()  # Random number from 0 to 1
        if (state_transition_probabilities_2.__contains__(pred)):
            cdf = cdfs_2[pred]
        else:
            print('found with order 1')
            cdf = cdfs_1[pred]
        cp = cdf[0][1]
        i = 0
        while rnd > cp:
            i += 1
            cp = cdf[i][1]

        nextWord = cdf[i][0]
        markov_chain.append(nextWord)
        #print('nextStep:', markov_chain)

    string = ' '.join(markov_chain)
    print('TEXT GENERATED: ',string)
    return string

def get_nouns(text):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    listOfNouns=[]
    for item in tagged:
        if item[1][0] == 'N':
            listOfNouns.append(item[0])
    return listOfNouns

# Function calls
raw_text = read_alice_in_wonderland()
state_transition_probabilities_1=markov_chain(raw_text, 1)
state_transition_probabilities_2=markov_chain(raw_text, 2)
start='time she'
length=10
Nouns=[]
while((len(Nouns))==0):
    generatedText = generate_2(state_transition_probabilities_1, state_transition_probabilities_2, length, start)
    Nouns = get_nouns(generatedText)
print('LIST OF NOUNS: ',Nouns)
concept = Nouns[0]

# also specified in _init_.py
from therex import TheRex
tr=TheRex()
#print(figures.keys())
#print(figures.items())
print('Concept:',concept)
# To obtain properties and categories of a given concept'''
general_categories = tr.member(concept)
#print(general_categories.keys())
categories=general_categories.get('category_heads')
#print(categories)
selected_category=common_modifier=(Counter(categories).most_common(3))[0][0]
print('selectedCategory:',selected_category)
extracted_modifiers = general_categories.get('modifiers')
#print('Modifiers:',extracted_modifiers)
selected_modifier=(Counter(extracted_modifiers).most_common(3))[0][0]
print('selectedModifier:',selected_modifier)

new_concepts = tr.category(selected_modifier,selected_category)
#print(new_concepts.keys())
new_categories=new_concepts.get('category_heads')
new_category=(Counter(new_categories).most_common(3))[0][0]
print('New Category:',new_category)

newer_concepts=tr.category(selected_modifier, new_category)
print(newer_concepts)
print(newer_concepts.keys())
newer_concepts=newer_concepts.get('category_heads')
finalConcept=(Counter(newer_concepts).most_common(3))[0][0]
print('Final Concept:', finalConcept)