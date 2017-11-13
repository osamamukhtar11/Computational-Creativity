Week 3 - Fictional Fact Generation
==================================

.. note::
    10.11.17 These assignments are still subject to change.

Introduction
------------

The paper `Baseline Methods for Automated Fictional Ideation <http://mark.granroth-wilding.co.uk/files/iccc2014.pdf>`_
describes some simple methods for generating fictional ideas. One of them, described in the section
*Fictional Ideation using ReVerb*, uses general-knowledge facts extracted from text with information extraction (IE)
techniques, and manipulates the facts to produce potentially interesting or amusing fictional ideas.

The method is simple and in itself barely qualifies as a creative system, being guided only by some simple statistics
and having no further representation at all of the meaning or value of the results. However, it can form one
generative component of a creative system and it demonstrates how NLP can be used to provide a knowledge resource
for creative processes.

In this week's exercises, you will implement the generative method. Instead of applying IE tools yourself, you
will use the output of a fairly recent system and write the code to manipulate facts to produce fictions.

Data
----
We will use facts output in the form of *relation triples* by the `ReVerb <http://reverb.cs.washington.edu/>`_
system. A large set of facts, produced by running the system over a large text corpus, is available to
`download <http://reverb.cs.washington.edu/reverb_clueweb_tuples-1.1.txt.gz>`_. However, it is large enough
to prohibit simply loading the whole set into memory and computing the statistics we need.

To simplify this, you can
`download a smaller, filtered set here <https://www.cs.helsinki.fi/u/magranro/cc2017/reverb.txt>`_.
This includes facts that appear to
be somewhat related to terms found in *Alice's Adventures in Wonderland* (the text you
used last week).

The Python module `factgen <https://github.com/assamite/cc-course-UH17/blob/master/week2/factgen.py>`_
contains some utilities for handling this data. Download it and put it in the same directory as your code,
so you can easily import it::

    >> import factgen

Exercises
---------

#. Write code to load the filtered set of ReVerb triples. You can use the ``read_triples()`` function::

      >> all_triples = factgen.read_triples("reverb.txt", min_attested=2)

   See the docstring for the meaning of ``min_attested``. You may want to adjust this parameter later on
   and see what effect it has.

   Build a list of all of the *entities* (the left-hand side or right-hand side of the triples).
   You can use the ``collect_entities()`` function to help with this.

   Prepare a list of some entities that you will use as input to the generation process. You may do
   this at this stage by manually selecting some entities of interest from those in the triples, or
   by programmatically randomly choosing some.

   Print out the facts about these entities, so you can get an idea of what your system will be starting
   from.

#. **RETURN** *(Code)* Implement the fact-manipulation technique described in
   `'Fictional Ideation using ReVerb' in the paper <http://mark.granroth-wilding.co.uk/files/iccc2014.pdf>`_,
   and introduced in Wednesday's lecture.

   You will need to write code to estimate the probability of a relation *r* given a LHS entity *X* (*p(r | X)*)
   and the probability of a RHS entity *Y* given a relation (*p(Y | r)*). Then you must compute these
   quantities for all possible relations and RHS entities, starting from one of your query terms on the LHS.

   Write a function ``generate_from_lhs(lhs, all_triples)`` that takes the LHS entity ``lhs`` and a list of
   triples, as read in above, ``all_triples`` and returns a list of new, generated triples ordered by descending
   score, together with their scores::

      >> rhs_replacements = generate_from_lhs(QUERY_TERM, all_triples)
      >> print("\nTop scoring made-up {}-related facts:\n{}".format(
          QUERY_TERM,
          "\n".join("{}, {}, {}  ({:.3f})".format(l, p, r, score) for (l, p, r, score) in rhs_replacements[:30])
      ))

      Top scoring made-up dinner-related facts:
      dinner, usually consists of, gift certificates  (0.100)
      dinner, consists of, grass  (0.067)
      dinner, consists of, nave  (0.067)
      dinner, consisted of, eggs  (0.050)
      dinner, consisted of, soup  (0.050)
      dinner, consisted of, cake  (0.050)

   *(Optional)* Also implement the corresponding function ``generate_from_rhs(rhs, all_triples)`` to generate
   triples given a RHS entity.

#. **RETURN** *(Text)* Take a look at the output of your generator, given several different queries as input.
   If all has gone well, you should find that some of the imaginary facts it outputs are at least a bit interesting
   or amusing. Others will be nonsensical or uninteresting (e.g. *dinner, consisted of, soup*).

   Why is this the case? How could this basic method be extended to increase the proportion of coherent and
   valuable outputs? Suggest some practical techniques that could be applied to achieve this.

   Focus in particular on simple methods that you would expect to get maximal improvements with minimal effort.
   If we were able to do reliable commonsense reasoning with broad-domain world knowledge, we could rule out
   *dinner, consisted of, soup* on the basis that it dinner often *does* consist of soup, but how can we perform
   (or approximate) this reasoning automatically using existing techniques or technologies?

   **You do not have to implement the methods!** By all means, do if you want and I'd love to see the result, but
   it's not required!

#. **RETURN** *(Text output)*
   `Download this text file <https://www.cs.helsinki.fi/u/magranro/cc2017/alice_with_triples.txt>`_
   and use it to train a new Markov model on this text, performing all the same preprocessing as you did before.
   It contains the full text of *Alice's Adventures in Wonderland*, plus text covering all of the words used
   in the ReVerb triples at least once (provided you set ``min_attested`` to ``2`` or more).

   Use your function ``generate_from_lhs`` (together with ``generate_from_rhs``, if you implemented it)
   to produce a small number of high-scoring output triples as before. Put together the three parts of
   each triple and split the words to produce a (roughly) tokenized sentence ``s``.

   Now use ``generate2``, with the transition probabilities trained on ``alice_with_triples.txt``, using the
   last two words of ``s`` as a start state. Add the generated words onto ``s`` to produce a longer sentence.

   You have now combined two generative methods in order to get an initial (sometimes) interesting seed from
   one and continue the story with another. These components could, of course, be combined with many other
   components to generate, modify, filter, expand, etc.

   Submit some examples of the output produced by your combined system, together with a brief analysis of
   what the system produced, its limitations and how they might be addressed. (A couple of sentences.)

#. **Exercise relating to paper not added yet**

#. **Exercise relating to paper not added yet**
