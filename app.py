from flask import request
from flask import render_template
from markov_chain import get_dict
from markov_chain import gen_markov_tweet
import json
from flask import Flask
from twitter_api import get_tweets
import html
from tweepy import TweepError

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", button_name="Go!")

    else:
        # get data from page
        user_input = html.escape(request.form['handle'])
        handle = "@" + user_input
        saved_dict = eval(request.form['lastUserDict'])

        if request.form['lastUser'] != user_input or user_input == "" or saved_dict == {}:
            # user entered new handle
            try:
                tweet_list = get_tweets(handle)
                saved_dict = get_dict(tweet_list)
                fake_tweet = gen_markov_tweet(saved_dict)

            except TweepError as err:
                # invalid or private handle

                if str(err) == "User is protected":
                    fake_tweet = "Error! User is private."
                else:
                    fake_tweet = "User not found! Please try another handle."

                saved_dict = {}

            except ValueError:
                # empty handle
                fake_tweet = "Please enter a handle."
                saved_dict = {}
        else:
            # user re-entered handle - use saved dict
            fake_tweet = gen_markov_tweet(saved_dict)

        return json.dumps({"handle": user_input, "tweet": fake_tweet, "saved_dict": str(saved_dict)})


if __name__ == "__main__":
    app.run()
