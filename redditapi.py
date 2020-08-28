import praw
import config
import re
import maps

def expand_contractions(word, contraction_map=maps.CONTRACTION_MAP):
    pass

def clean_text(text):
    # Regex terms
    tag_re = re.compile(r'^\[.*?\]', re.IGNORECASE)
    ytlink_re = re.compile(r'\[(http).*?\]', re.IGNORECASE)
    symbol_re = re.compile(r'[\.\^\$\*\+\?\{\}\[\]\\\|\(\)\-\@\:]', re.IGNORECASE)

    cleaned = text
    mo = tag_re.search(cleaned)
    if mo:
        cleaned = cleaned.replace(mo.group(), '')
    mo = ytlink_re.search(cleaned)
    if mo:
        cleaned = cleaned.replace(mo.group(), '')
    mo = symbol_re.findall(cleaned)
    for symbol in mo:
        cleaned = cleaned.replace(symbol, '')

    # Expand contractions
    # maybe get rid of possessives
    return cleaned

def get_titlewords_topalltime(subreddit):
    """
    Accepts a subreddit and returns the word occurances of the words found in the titles
    of the first 1000 posts when sorted by Top.
    """
    r = praw.Reddit(user_agent=config.user_agent, client_secret=config.client_secret, client_id=config.client_id)
    word_occurances = {}
    
    for submission in r.subreddit(subreddit).top(limit=100):
        title = clean_text(submission.title)
        # tokenize
        # add to dict if key doesnt exist, if it does, increment frequency



        print(title.strip())
    # return word_occurances


get_titlewords_topalltime("machinelearning")

#TODO: Implement checkboxes on the front end so the user can choose to sort by new, top, hot etc
#TODO: allow the user to select comments or titles for the posts