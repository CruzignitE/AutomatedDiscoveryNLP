import spacy
from collections import Counter
from sacremoses import MosesDetokenizer

'''
pip install spacy && python -m spacy download en
'''


class SpacyTest:



    print("-----Spacy-----")
    NLP = spacy.load("en")
    print(type(NLP))

    @classmethod
    def test1(cls):

        # Import file
        l_raw_text = ""
        with open("Test_Input/75_raw.txt", 'r') as l_file:

            # Raw Text
            l_raw_text = l_file.read().replace('\n', '')
            l_file.close()

        # l_raw_text = "While Samsung has expanded overseas, South Korea is still host to most of its factories and research engineers."

        print("-----Raw-----")
        print(type(l_raw_text))
        print("..." + l_raw_text[395:500] + "...")

        print("-----Doc-----")
        l_doc = SpacyTest.NLP(l_raw_text)
        print(type(l_doc))
        assert isinstance(l_doc, spacy.tokens.doc.Doc)

        print("-----Word tokens-----")
        l_word_tokens = [l_token.text for l_token in l_doc]
        print(type(l_word_tokens))
        print(l_word_tokens)

        print("-----Sentence tokens-----")
        l_sentence_tokens = list(l_doc.sents)
        print(type(l_sentence_tokens))
        print(l_sentence_tokens)

        print("-----Stop words and punctuation and lemmas and pos-----")
        l_pos_tokens = [(l_token.lemma_, l_token.pos_) for l_token in l_doc
                        if l_token.is_stop is not True and l_token.is_punct is not True]
        print(type(l_pos_tokens))
        print(l_pos_tokens)

        print("-----Token info-----")
        for l_token in l_doc:
            print(l_token.text, l_token.lemma_, l_token.pos_, l_token.tag_, l_token.dep_,
                  l_token.shape_, l_token.is_alpha, l_token.is_stop, l_token.ent_type_, l_token.norm_)


        print("-----Word freq-----")
        l_word_freq = Counter(l_word_tokens)
        print(type(l_word_freq))
        l_common_words = l_word_freq.most_common(5)
        print(l_common_words)

        print("-----NER-----")
        l_labels = set([l_word.label_ for l_word in l_doc.ents])
        for l_label in l_labels:
            l_entities = [l_entity.string for l_entity in l_doc.ents if l_label == l_entity.label_]
            l_entities = list(set(l_entities))
            print(l_label, l_entities)

        print("Done")







 # ----Main method ----

def main():
    SpacyTest.test1()
    print("Done!")

    # Define main method

if __name__ == '__main__':
    main()