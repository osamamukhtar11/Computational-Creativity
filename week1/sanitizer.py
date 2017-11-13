# IMPROVEMNTS:
# Lowercase all tokens t avoid duplicates.
# Separate based on punctuation like ' to allow not or n't to be given equal chance

import re
import nltk
import string

def sanitize_list_of_tokens(tokenized_sentences):
    sanitized_sentences = []
    is_word = re.compile('\w')
    for sent in tokenized_sentences:
        eachSentence = ' '.join(e for e in sent)
        eachSentence=eachSentence.lower()
        eachSentence.translate(string.punctuation)
        sent = nltk.word_tokenize(eachSentence)
        sanitized = [token for token in sent if is_word.search(token)] + ['.']
        sanitized_sentences.append(sanitized)
        return sanitized_sentences


text = "I've always wanted Ali's car but I couldn't have gotten it"


# And replace more than one subsequent whitespace chars with one space
text = re.sub(r'\s+', ' ', text)

# Tokenize the text into sentences.
sentences = nltk.sent_tokenize(text)

# Tokenize each sentence to words. Each item in 'words' is a list with
# tokenized words from that list.
tokenized_sentences = []
for s in sentences:
    w = nltk.word_tokenize(s)
    tokenized_sentences.append(w)

# Next, we sanitize the 'words' somewhat. We remove all tokens that do not have
# any Unicode word characters, and force each sentence's last token to '.'.
# You can try other sanitation methods (e.g. look at the last sentence).

sanitized_sentences=sanitize_list_of_tokens(tokenized_sentences)
print(sanitized_sentences)