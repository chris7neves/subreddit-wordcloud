import praw
import config
import re
from maps import CONTRACTION_MAP
import unicodedata
from nltk.corpus import stopwords
from nltk import word_tokenize


def expand_contractions(text, c_map=CONTRACTION_MAP):
    """
    Receives a submission title as text, returns title with expanded contractions.
    """
    contractions_re = re.compile('({})'.format('|'.join(c_map.keys())), 
                                flags=re.IGNORECASE|re.DOTALL)
    mo = contractions_re.findall(text)
    if mo:
        for contraction in mo:
            first_char = contraction[0]
            expanded = CONTRACTION_MAP.get(contraction.lower())

            if expanded:
                replaced = first_char + expanded[1:]
                text = text.replace(contraction, replaced, 1)
            else:
                # Change this to log the error when logging system is implemented
                print("The following contraction cannot be expanded: {}".format(contraction))
    return text

def standardize_to_unicode(text):
    """
    Author: Kerry Parker
    Date: August 30th, 2020
    Availability: https://towardsdatascience.com/creating-word-clouds-with-python-f2077c8de5cc

    Standardizes text formatting and gets rid of special characters, like accents.
    """
    unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def remove_ytlink(text):
    # ytlink_re = re.compile(r'http|https|ftp|ftps\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(\/\S*)?',
    #                          re.IGNORECASE)
    ytlink_re = re.compile(r'((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$')
    mo = ytlink_re.search(text)
    if mo:
        text = text.replace(mo.group(), '')
    return text

def remove_tag(text):
    tag_re = re.compile(r'\[.*?\]', re.IGNORECASE)
    mo = tag_re.findall(text)
    if mo:
        for tag in mo:
            text = text.replace(tag, '')
    return text

def remove_symbol(text):
    symbol_re = re.compile(r'[\.\,\;\"\'\“\”\^\$\*\/\+\?\{\}\[\]\\\|\(\)\-\—\@\:\!\#\%\&\=\_]', re.IGNORECASE)
    mo = symbol_re.findall(text)
    if mo:
        for symbol in mo:
            text = text.replace(symbol, '')
    return text

def remove_possesive(text):
    possesive_re = re.compile(r'(\'|\’)s')
    text = possesive_re.sub('', text)
    return text

def clean_text(text):

    # Remove youtube links
    text = remove_ytlink(text)

    # Remove tags
    text = remove_tag(text)

    # Expand contractions, should come before remove possesives
    text = expand_contractions(text)

    # Remove posessives, must come before remove symbols
    text = remove_possesive(text)

    # Remove special symbols, must come after remove possesives and expand contractions
    text = remove_symbol(text)

    # remove accents and non standard characters
    text = standardize_to_unicode(text)

    # Convert to lower case and remove trailing white space
    text.lower()
    text.strip()

    return text

def get_titlewords_topalltime(subreddit):
    """
    Accepts a subreddit and returns the word occurances of the words found in the titles
    of the first 1000 posts when sorted by Top.
    """
    r = praw.Reddit(user_agent=config.user_agent, client_secret=config.client_secret, client_id=config.client_id)
    word_occurances = {}

    stopword_list = stopwords.words('english')
    
    for submission in r.subreddit(subreddit).top(limit=1000):
        title = clean_text(submission.title)

        for word in word_tokenize(title):
            word = word.strip()
            word = word.lower()
            if word in stopword_list or word.isdigit():
                continue
            if word_occurances.get(word) is None:
                word_occurances[word] = 1
            else:
                word_occurances[word] += 1
    
    # Sort word_occurances by word occurance in descending order
    word_occurances = {k: v for k, v in sorted(word_occurances.items(), key=lambda item: item[1], reverse=True)}

    for key, value in word_occurances.items():
        print("{}: {}".format(key, value))
    # return word_occurances


get_titlewords_topalltime("machinelearning")
#print(expand_contractions("Y'all can't expand contractions I'd think"))
#print(remove_symbol("hello \"Test\""))
#print(clean_text("[D][R] A letter urging Springer Nature not to publish “A Deep Neural Network Model to Predict Criminality Using Image Processing”"))
#print(type(word_tokenize("If you say in a paper you provide code it should be required to be available at time of publication")))



#TODO: Implement checkboxes on the front end so the user can choose to sort by new, top, hot etc
#TODO: allow the user to select comments or titles for the posts