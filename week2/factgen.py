"""
Tools for implementing a simple version of the (probably) fictional fact generation method
described in:
    Baseline Methods for Automated Fictional Ideation (2014), Llano et al., ICCC

Use the tools provided here in the week 2 assignment.

"""
from collections import Counter


def read_triples(filename, min_attested=0):
    """
    Reads in triples from a TSV file, of the form distributed by OpenIE. A small dataset, constructed
    from one distributed by the University of Washington, is provided for you to use in your exercise.

    Note that everything is lowercased, so you should lowercase your queries as well.

    """
    with open(filename, "r") as f:
        data = f.read()
    fields = [line.split("\t") for line in data.split("\n") if line]
    # The LHS, predicate and RHS are in columns 1 to 3
    # Col 7 contains the number of attestations during extraction: filter out those with very few
    # Make them all lowercase, for ease of querying
    return [(row[1].lower(), row[2].lower(), row[3].lower()) for row in fields if int(row[7]) >= min_attested]


def collect_entities(triples, min_freq=0):
    """
    Given a list of triples, as returned by ``read_triples()``, collect the entities used on the LHS
    and RHS of the facts, filtering out ones that occur rarely.

    """
    terms = sum(([l, r] for (l, p, r) in triples), [])
    term_counts = Counter(terms)
    # Select a query term from those that have at least a few facts about them
    freq_terms = list(set(t for (t, c) in term_counts.items() if c >= min_freq))
    return freq_terms
