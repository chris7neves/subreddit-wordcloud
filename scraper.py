import praw
import pandas as pd
import config
from flask import Flask, render_template



r = praw.Reddit(user_agent=config.user_agent, client_secret=config.client_secret, client_id=config.client_id)

subreddit = 'machinelearning'
top_posts = r.subreddit(subreddit).top(limit=10)

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', top_posts=top_posts)

if __name__ == '__main__':
    app.run(debug=True)