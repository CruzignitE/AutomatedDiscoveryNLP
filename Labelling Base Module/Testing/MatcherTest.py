import spacy
from collections import Counter
from sacremoses import MosesDetokenizer
from spacy import displacy
from pathlib import Path
from spacy.matcher import Matcher

class MatcherTest:

    @classmethod
    def test(cls):
        nlp = spacy.load("en_core_web_sm")
        matcher = Matcher(nlp.vocab)
        # Add match ID "HelloWorld" with no callback and one pattern
        pattern = [{"LOWER": "hello"}, {"IS_PUNCT": True}, {"LOWER": "world"}]
        matcher.add("Hello World Matcher", None, pattern)

        doc = nlp(u"Hello, world! Hello, world! My name is John")
        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)
            print(doc[start:end])

        ner = nlp.get_pipe("ner")
        ner.add_label("VEGETABLE")

        ents = list(doc.ents)
        print(ents)
        print(ents[0])
        print(type(ents[0]))

        print(doc[0:5])


        print(type(ents))
        print(ents)

        for ent in doc.ents:
            print(type(ent))
            print(ent)

        for token in doc:
            print(type(token))

        print("Done!")

# ----Main method ----

def main():
    MatcherTest.test()
    print("Done!")

    # Define main method

if __name__ == '__main__':
    main()