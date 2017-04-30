import tweepy
from flask import Flask
from flask import request
from flask import render_template
from config import Secrets
from tweet_generator import get_tweet
import re

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", button_name="Go!")
    else:
        inputUser = request.form['userValue']
        inputUser = inputUser.replace("<br>", "")

        user = "@" + inputUser

        auth = tweepy.OAuthHandler(Secrets.api_key, Secrets.api_secret)
        auth.set_access_token(Secrets.access_token, Secrets.access_token_secret)

        api = tweepy.API(auth)
        tweet_string = ""

        emoji_pattern = re.compile(u'['
                          u'\U0001F300-\U0001F64F'
                          u'\U0001F680-\U0001F6FF'
                          u'\u2600-\u26FF\u2700-\u27BF]+',
                          re.UNICODE)

        other_pattern = re.compile(r'@\w+\s?|\s?http[\w:/\.]+|\*|"|\(|\)|:\)|:\(|-')

        try:
            for status in tweepy.Cursor(api.user_timeline, screen_name=user, include_rts=False).items(500):
                # regex out handles, links, asterisks, quotes, parentheses, smiley faces
                tweet = re.sub(other_pattern, "", status._json['text'])
                tweet = re.sub(emoji_pattern, "", tweet)
                tweet = tweet.strip()
                # add period if necessary
                if len(tweet) > 1 and tweet[-1] not in ["?", "!", "."]:
                    tweet += "."

                tweet_string += tweet + " "

            # make word all lowercase unless it's all uppercase
            tweet_string = " ".join([(w.lower() if w != w.upper() else w) for w in tweet_string.split()])

            fake_tweet = get_tweet(tweet_string)

        except:
            fake_tweet = "Is that a valid handle? Try again!"

        return render_template("index.html", button_name="Again!", tweet=fake_tweet, user=inputUser)


if __name__ == "__main__":
    app.run()