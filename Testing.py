import nltk
from nltk import word_tokenize

class Testing:

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


        #x = nltk.Text(text_file)
        #x = nltk.Text("hello world")
        #text_file.close()
        #print(text_file.readlines())
        #print("Text:")
        #print(x)
       # print("Concordance:")
        #x.concordance("hello")


# ----Main method----
def main():
    Testing.test1()
    print("Done!")


# Define main method
if __name__ == '__main__':
    main()

