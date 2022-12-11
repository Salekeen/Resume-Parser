# Importing dependencies
import spacy
from spacy.matcher import Matcher
import re
import os


def get_Name(doc):
    """
    It takes a spaCy document as input, and returns the first person's name it finds in the document
    
    :param doc: The document we want to extract the name from
    :return: The name of the person.
    """

    name = ''
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            name = entity.text
            break
    return name.split('\n')[0]


def get_email(doc):
    """
    - Create a pattern that matches an email address
    - Create a matcher object
    - Add the pattern to the matcher
    - Use the matcher to find matches in the text
    - Return the first match
    
    Let's try it out:
    
    :param doc: The document we want to extract the email from
    :return: The email address
    """

    pattern = [{"TEXT": {"REGEX": "[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+"}}]

    matcher = Matcher(nlp.vocab)
    matcher.add("Email", [pattern])

    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text


def get_phoneNumber(doc):
    """
    It takes a doc as input, creates a pattern, creates a matcher, adds the pattern to the matcher,
    matches the pattern to the doc, and returns the span
    
    :param doc: The document we want to extract the phone number from
    :return: The phone number
    """

    pattern = [{"TEXT": {"REGEX": "[+0-9]{10,14}"}}]
    matcher = Matcher(nlp.vocab, validate=True)
    matcher.add("PhoneNumber", [pattern])
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text
        break


def get_education_degree(doc):
    """
    - We use a regular expression to find all instances of the word "M.S." or "B.S." or "H.S." or "S.S."
    in the text.
    - We then use the `doc.char_span()` function to find the actual span of the word in the text.
    - We then append the span to a list of degrees
    
    :param doc: The document we want to extract the entities from
    :return: A list of strings
    """

    degrees = []
    expression = r"\b[MmBHhSs][.]?[Ss][.]?[Cc][.]?\b"
    for match in re.finditer(expression, doc.text):
        start, end = match.span()
        span = doc.char_span(start, end)

        if span is not None:
            degrees.append(span.text)
    return degrees


def get_university_name(doc):
    """
    It takes a spacy doc object as input and returns a list of university names
    
    :param doc: The document we want to extract entities from
    :return: A list of the university names
    """

    uni = []
    for ent in doc.ents:
        if "University" in ent.text:
            uni.append(ent.text.split('\n')[0])
            return uni


if __name__ == "__main__":

    extracted_texts_dir = '/home/epsilondelta/Work/ocr-project/extracted_texts'

    # defining spacy language model
    nlp = spacy.load("en_core_web_lg")

    for file in os.listdir(extracted_texts_dir):
        text = ''
        f = open(os.path.join(extracted_texts_dir, file), 'r')
        for x in f:
            text += x

        doc = nlp(text)

        print(get_email(doc))
        print(get_Name(doc))
        print(get_phoneNumber(doc))
        print(get_education_degree(doc))
        print(get_university_name(doc))
        print("*********")
