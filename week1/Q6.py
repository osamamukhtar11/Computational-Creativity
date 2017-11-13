import re
import nltk
import string
import os
import random

def sanitize_list_of_tokens(tokenized_sentences):
    sanitized_sentences = []
    is_word = re.compile('\w')
    for sent in tokenized_sentences:
        eachSentence = ' '.join(e for e in sent)
        eachSentence = eachSentence.lower()
        eachSentence.translate(string.punctuation)
        sent = nltk.word_tokenize(eachSentence)
        sanitized = [token for token in sent if is_word.search(token)] + ['.']
        sanitized_sentences.append(sanitized)

    return sanitized_sentences

def markov_chain(raw_text, sanitize):
    raw_text = re.sub(r'\s+', ' ', raw_text)
    # Tokenize the text into sentences.
    sentences = nltk.sent_tokenize(raw_text)

    # Tokenize each sentence to words. Each item in 'words' is a list with
    # tokenized words from that list.
    tokenized_sentences = []
    for s in sentences:
        w = nltk.word_tokenize(s)
        tokenized_sentences.append(w)

    if (sanitize):
        tokenized_sentences = sanitize_list_of_tokens(tokenized_sentences)

    transitions = {}
    for eachList in tokenized_sentences:
        # eachSentence = ' '.join(e for e in eachList)
        for i in range(len(eachList) - 1):
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

# And replace more than one subsequent whitespace chars with one space
raw_text = re.sub(r'\s+', ' ', alice)

#raw_text = "I have a dream. You have no dream but I have a dream. I am dreamer. We do not want to fall. But we fall in no land."
probabilities_dict=markov_chain(raw_text, True)

# for pred in probabilities_dict:
#     sorted_by_values = sorted(probabilities_dict[pred].items(), key=operator.itemgetter(1), reverse=True)
#     print(pred, sorted_by_values)



# Q6 in assignment
def generate(state_transition_probabilities, length=10, start=None):
     if(start==None):
         start = random.choice(list(state_transition_probabilities.keys()))

     cdfs = make_cdfs_from_probs(probabilities_dict)
     markov_chain=[start]
     print('start:',markov_chain)
     i=0
     while len(markov_chain) < length and markov_chain[len(markov_chain)-1]!='.':
         pred=markov_chain[len(markov_chain)-1]   # last element of text
         #print('pred:',pred)
         rnd = random.random()  # Random number from 0 to 1
         #print('cdfs:',cdfs)
         cdf = cdfs[pred]
         #print('cdfs[pred]',cdf)
         cp = cdf[0][1]
         #print('cdf[0][1]',cp)
         i = 0
         while rnd > cp:
             i += 1
             cp = cdf[i][1]
             #print(i,'_',cp)

         #print(i, '_', cp, cdf[i][0])
         #print(cdf[i][0])
         nextWord = cdf[i][0]
         #print(nextWord)
         markov_chain.append(nextWord)
         print('nextStep:',markov_chain)

     string = ' '.join(markov_chain)
     print(string)
     return string
#
generate(probabilities_dict, 10, None)