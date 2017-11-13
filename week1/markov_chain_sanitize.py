import re
import nltk
import string
import operator

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

raw_text = "I've a dream. You have a Dream. We have a dream."
probabilities_dict=markov_chain(raw_text, True)

for pred in probabilities_dict:
    sorted_by_values = sorted(probabilities_dict[pred].items(), key=operator.itemgetter(1), reverse=True)
    print(pred, sorted_by_values)

