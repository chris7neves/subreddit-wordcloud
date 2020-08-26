import praw
import config


def GetTitleWordsTop(subreddit):
    """
    Accepts a subreddit and returns the word occurances of the words found in the titles
    of the first 1000 posts when sorted by Top.
    """
    r = praw.Reddit(user_agent=config.user_agent, client_secret=config.client_secret, client_id=config.client_id)
    sub = r.get_subreddit(subreddit)
    word_occurances = []
    return word_occurances

#TODO: Implement checkboxes on the front end so the user can choose to sort by new, top, hot etc
#TODO: allow the user to select comments or titles for the posts