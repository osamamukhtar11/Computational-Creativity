Week 2 - Markov Chains (cont.) and Metaphor Generation
======================================================

.. note::
    (6.11.17 13:57) The exercises are now in their final form!

Exercises
---------

#. **RETURN** *(Code)* Return to your code from last week's exercises, where you trained a Markov model
   on the text of *Alice's Adventures in Wonderland*.

   Alter your function ``markov_chain`` to accept an optional parameter ``order`` which
   specifies the order of the Markov chain to be created.

   That is, with ``order=2`` a state contains two successive tokens from the same sentence.

#. **RETURN** *(Code)* Create a new version of your function ``generate``,
   ``generate2(probs1, probs2, length=10, start=None)``. ``probs1`` and ``probs2`` are now expected to be the
   state transition distributions for an order-1 and an order-2 Markov model, respectively.

   This function should generate from the Markov model as before, except that, if it encounters a context
   of two words that does not exist in the order-2 model's distribution, it uses the order-1 model instead,
   treating just the single latest word as context.

   This is a form of a commonly used technique when working with Markov models, known as *backoff*.

#. **RETURN** *(Code)* Use ``nltk``'s ``pos_tag``, refer to :doc:`parsing_NLTK`, to obtain all nouns in the output of your ``generate2``.
   If the generated text did not contain any nouns, re-generate it again until it contains at least one noun.

#. **RETURN** *(Code)* Select a noun as a target concept from the nouns obtained in the previous exercise question.
   Implement the approach described in Galvan et al. (2016), under *Process* section, for generating rhetorical
   figures. The approach utilizes `Thesaurus Rex (v2) <http://ngrams.ucd.ie/therex2/>`_'s API to retrieve
   categories and adjectival properties of the target concept, and search for potential source concepts.

    .. note::
        Use the class ``TheRex`` implemented in `therex.py <https://github.com/assamite/cc-course-UH17/blob/master/week2/therex.py>`_
        to access Thesaurus Rex's web service. The library requires ``requests`` and ``xmltodict`` python packages. To install them,
        execute ``pip install requests xmltodict`` in your terminal (and virtual environment).

        Below is a sample code of using the class:

		>>> from therex import TheRex
		>>> tr = TheRex()
		>>> tr.member('cat') # get properties and categories of a cat
		>>> tr.category('furry', 'animal') # furry concepts in animal category

        Remember that Thesaurus Rex is a proof-of-concept web service, so use
        *throttling* when accessing it. That is, add a little pause between your
        calls when querying it in a loop.

#. **RETURN** *(Code)* Use the analogy template "**{TARGET} is as {PROP} as {SOURCE}**" to construct a figurative sentence.
   Then, output the generated figurative sentence after the text produced by your Markov chain model.

#. Alter the category selection method from random selection to
   randomly selecting a category that also contains the target concept.
   After that try out randomly selecting a category that does not contain the target concept. Based on your observations,
   which method seems to produce better figurative sentences?

#. **RETURN** *(Text)* How would you employ the above approach in a creative system producing poems?
   Write a brief outline of your approach.

#. **RETURN** *(Text)* Analyze the creativity of the above analogy generator using
   Boden's (1992) three types of creativity, refer to slides of first week
   (`1 <https://courses.helsinki.fi/sites/default/files/course-material/4524022/CompCreativityToivonen_30_10_2017.pdf>`_
   and `2 <https://courses.helsinki.fi/sites/default/files/course-material/4524230/CompCreativityToivonen_1-11-2017b.pdf>`_).
