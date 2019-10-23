import spacy
from collections import Counter
from sacremoses import MosesDetokenizer
from spacy import displacy
from pathlib import Path

class EntityTest:

    TEXTS2 = [
        "In respect to the cannabis that was found, you are sentenced on the basis that that was a small amount for your own use."
        "In August 2015 and November 2015, you were sentenced to short periods of imprisonment. "
        "In defence submissions, your counsel submitted that the appropriate sentence would be a sentence of imprisonment, to be followed by a community correction order."
        "I declare that you have served 175 days of this sentence by way of pre-sentence detention. "
        "On Charge 13 of dealing with the proceeds of crime, you are convicted and sentenced to two months' imprisonment."
        "That is the sentence that I impose upon you, Mr Bowden."
        "But for your plea of guilty and the operation of s.6AAA of the Sentencing Act 1991, I would have sentenced you to five years' imprisonment with a three-year minimum term."
        "In the circumstances of your case, I propose to convicted you of the offence of aggravated burglary and sentence you to a term of imprisonment of 18 months."
        "Immediately following your release, I sentence you to a community corrections order for a period of a further 24 months with a condition that you perform 200 hours of unpaid community work and that you receive appropriate mental health assessment and treatment as may be required during the period of that order, and those conditions are in addition to the core conditions attaching to a community corrections order which you have agreed to in the course of your assessment and which I am told by Mr Power you agree to today.  "
        "Sentence: Convicted and sentenced to Total Effective Sentence 9 years and 1 month’s imprisonment with non-parole period of 6 years and 6 months’ imprisonment – s.6AAA Sentencing Act 1991 declaration – Pre-sentence detention 280 days – Ancillary order Disposal order"
        "I state that but for your pleas of guilty I would have imposed a sentence of eight and a half years with a minimum non-parole period of six and a half years."
        "I make the following declaration pursuant to s.6AAA:  but for your plea of guilty I would have convicted and sentenced you to 12 months' imprisonment to follow a three-year Community Correction Order.  "
        "In respect to the two charges on the indictment an aggregate sentence will be imposed because it represents one course of conduct over a short period of time on the date set out on the indictment.  "
        "Sentence: 10 months imprisonment (302 days PSD) to be followed by a CCO of 2 years duration with unpaid community work, rehabilitative and supervision conditions."
        "I direct that one month of the sentence on the two summary charges of unlicensed driving be served - it's actually driving whilst disqualified - I have come to realise."
        "One month of the aggregate sentence on the charges of driving whilst disqualified be served cumulatively on the sentence imposed on the indictment this day, otherwise the sentences will be served concurrently with all other sentences imposed this day.  "
    ]

    TEXTS1 = [
        "The total overall sentence is therefore 11 months' imprisonment to be followed by a two year CCO, and I will go back over the conditions shortly.",
        "Overall I have concluded the most appropriate sentence to punish you is a Community Correction Order and not an immediate term of imprisonment to be served, as sought by the Crown.  ",
        "It being conceded that an aggregate sentence is appropriate by your counsel and the learned prosecutor, I sentence you on all three charges and the summary charge, to a total effective sentence of six and a half years' imprisonment.",
        "I direct that one year from the sentences on charges 2 and 3, and six months from the sentences on charges 4 and 5, as well as one month from the summary charge, be served cumulatively with each other and with the base sentence, producing a total effective sentence of nine years and one month imprisonment and I direct that you serve six years, six months’ imprisonment before becoming eligible for parole.",
        "I fix no minimum period so you will be required to serve 18 months.",
        "The total effective sentence is four years and nine months."
    ]

    TEXTS = [
        "Net income was $9.4 million compared to the prior year of $2.7 million.",
        "Revenue exceeded twelve billion dollars, with a loss of $1b.",
    ]




    seen_tokens = set()
    nlp = spacy.load("en_core_web_sm")

    @classmethod
    def test2(cls):
        # sentences = [u"Net income was $9.4 million compared to the prior year of $2.7 million."]
        l_counter = 1
        for sent in cls.TEXTS1:
            doc = cls.nlp(sent)

            # displacy.serve(doc, style="dep")

            svg = displacy.render(doc, style="dep")
            file_name = "(Legal)(Dep) Example" + str(l_counter) + ".svg"
            output_path = Path("Images/" + file_name)
            output_path.open("w", encoding="utf-8").write(svg)

            svg = displacy.render(doc, style="ent")
            file_name = "(Legal)(Ent) Example" + str(l_counter) + ".svg"
            output_path = Path("Images/" + file_name)
            output_path.open("w", encoding="utf-8").write(svg)

            l_labels = set([l_word.label_ for l_word in doc.ents])
            for l_label in l_labels:
                l_entities = [l_entity.string for l_entity in doc.ents if l_label == l_entity.label_]
                l_entities = list(set(l_entities))
                print(l_label, l_entities)

            l_counter += 1

            ents = list(doc.ents)
            print("TEST: " + str(ents))

            print("-----")
            for money in filter(lambda w: w.ent_type_ == "MONEY", doc):
                print(money.text + " (" + money.pos_ + ", " + money.dep_ + ")")



        # print(spacy.displacy.render(doc, style="ent", page="true"))


    @classmethod
    def test(cls):


        for text in cls.TEXTS:
            doc = cls.nlp(text)
            relations = cls.extract_currency_relations(doc)
            for r1, r2 in relations:
                print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))

    @classmethod
    def filter_spans(cls, spans):
        # Filter a sequence of spans so they don't contain overlaps
        get_sort_key = lambda span: (span.end - span.start, span.start)
        sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
        result = []
        cls.seen_tokens = set()
        for span in sorted_spans:
            if span.start not in cls.seen_tokens and span.end - 1 not in cls.seen_tokens:
                result.append(span)
                cls.seen_tokens.update(range(span.start, span.end))
        return result

    @classmethod
    def extract_date_relations(cls, doc):
        # Merge entities and noun chunks into one token
        cls.seen_tokens = set()
        spans = list(doc.ents) + list(doc.noun_chunks)
        spans = cls.filter_spans(spans)
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)

        relations = []
        for money in filter(lambda w: w.ent_type_ == "MONEY", doc):
            if money.dep_ in ("attr", "dobj"):
                subject = [w for w in money.head.lefts if w.dep_ == "nsubj"]
                if subject:
                    subject = subject[0]
                    relations.append((subject, money))
            elif money.dep_ == "pobj" and money.head.dep_ == "prep":
                relations.append((money.head.head, money))
        return relations


    @classmethod
    def extract_currency_relations(cls, doc):
        # Merge entities and noun chunks into one token
        cls.seen_tokens = set()
        spans = list(doc.ents) + list(doc.noun_chunks)
        spans = cls.filter_spans(spans)
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)

        relations = []
        for money in filter(lambda w: w.ent_type_ == "MONEY", doc):
            if money.dep_ in ("attr", "dobj"):
                subject = [w for w in money.head.lefts if w.dep_ == "nsubj"]
                if subject:
                    subject = subject[0]
                    relations.append((subject, money))
            elif money.dep_ == "pobj" and money.head.dep_ == "prep":
                relations.append((money.head.head, money))
        return relations




# ----Main method ----

def main():
    EntityTest.test()
    EntityTest.test2()
    print("Done!")

    # Define main method

if __name__ == '__main__':
    main()