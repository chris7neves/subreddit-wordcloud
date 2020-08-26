import config
from flask import Flask, render_template, redirect, flash, url_for, session
from forms import SubredditSelect



# r = praw.Reddit(user_agent=config.user_agent, client_secret=config.client_secret, client_id=config.client_id)

# subreddit = 'machinelearning'
# top_posts = r.subreddit(subreddit).top(limit=10)

top_posts = ['this is the first', 'this is the second', 'this is the third', 'this is the fourth', 'this is the fifth']

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SubredditSelect()
    if form.validate_on_submit():
        session['subreddit'] = form.subreddit.data
        return redirect(url_for('results'))
    return render_template('home.html', top_posts=top_posts, title='CloudData', form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
    return render_template('results.html', subreddit=session.pop('subreddit', None))

@app.route('/more', methods=['GET'])
def more():
    return render_template('more.html', title='CloudData')

if __name__ == '__main__':
    app.run(debug=True)