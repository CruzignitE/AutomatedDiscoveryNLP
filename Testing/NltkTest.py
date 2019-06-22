import nltk, re, pprint
from nltk import word_tokenize


class NltkTest:

    @classmethod
    def test1(cls):

        # Import file
        with open("Resources/Output/Formatted/Test.txt", 'r') as l_file:
            # Raw Text
            l_raw_text = l_file.read()
            print("-----Raw-----")
            print(type(l_raw_text))
            print("..." + l_raw_text[395:500] + "...")

        # Tokenize
        l_tokens = word_tokenize(l_raw_text)
        print("-----Tokens-----")
        print(type(l_tokens))
        print("..." + str(l_tokens[400:420]) + "...")

        # Text
        print("-----Text-----")
        l_text = nltk.Text(l_tokens)
        print(type(l_text))

        print("~~~~~Collocations~~~~~")
        l_text.collocations()

        print("~~~~~Concordance~~~~~")
        l_text.concordance("sentence")

        print("~~~~~Common Contexts~~~~~")
        l_text.common_contexts(["sentence"])

        print("~~~~~Names File~~~~~")
        l_names_corpus = nltk.corpus.names
        print(type(l_names_corpus))
        print(l_names_corpus)

        print("~~~~~Revert back to tokens~~~~~")
        l_tokens = l_text.tokens
        print("..." + str(l_tokens[400:420]) + "...")
        print(type(l_tokens))

        print("~~~~~Tagging~~~~~")
        l_tags = nltk.pos_tag(l_text)
        print(type(l_tags))
        print([s for s in l_tags[400:420]])
        l_text.similar("charge")






# ----Main method----
def main():
    NltkTest.test1()
    print("Done!")


# Define main method
if __name__ == '__main__':
    main()

    '''
   Send a message to a recipient

   :param str sender: The person sending the message
   :param str recipient: The recipient of the message
   :param str message_body: The body of the message
   :param priority: The priority of the message, can be a number 1-5
   :type priority: integer or None
   :return: the message id
   :rtype: int
   :raises ValueError: if the message_body exceeds 160 characters
   :raises TypeError: if the message_body is not a basestring
   '''