import tweepy
import re
from config import Secrets
from tweepy import TweepError


def get_tweets(handle):
    """ :param handle: a non-empty string starting with @
        :return: a list of words in tweets from the specified user
    """

    if handle == "@":
        raise ValueError
    else:
        # connect to API
        auth = tweepy.OAuthHandler(Secrets.api_key, Secrets.api_secret)
        auth.set_access_token(Secrets.access_token, Secrets.access_token_secret)

        api = tweepy.API(auth)
        
        # check if they're protected
        is_protected = api.get_user(handle).protected

        if is_protected:
            raise TweepError("User is protected")

        # pre-compile regex pattern
        regex_pattern = re.compile(r"""
                                    @[\w\']+             # handles
                                    |http[\w:/\.]+       # links
                                    |\*                  # asterisks
                                    |"|''                # quotes
                                    |\(|\)               # parentheses
                                    |\[|\]               # brackets
                                    |:\)|:\(             # smiley faces
                                    |,                   # commas
                                    |…                   # ...
                                    |&[A-Za-z;]+         # html special entities
                                    """, re.VERBOSE)

        # loop through tweets
        tweet_list = []
        for status in tweepy.Cursor(api.user_timeline, screen_name=handle, include_rts=False).items(500):
            # grab tweet from response
            tweet = status.text

            # clean up tweet and make it a list
            tweet_list += get_cleaned_list(tweet, regex_pattern)

        # return list containing all tweets
        return tweet_list


def get_cleaned_list(tweet, regex_pattern):
    """ :param tweet: a tweet in the form of a string
        :param regex_pattern: pre-compiled regex pattern
        :return: cleaned tweet, represented as a list
    """

    tweet = re.sub(regex_pattern, "", tweet)
    words = tweet.split()

    for i in range(len(words)):
        # if a word isn't all capitals, make it all lowercase
        #if words[i].upper() != words[i]:
        #    words[i] = words[i].lower()

        # strip whitespace
        words[i] = words[i].strip()

    # add period of necessary
    if len(words) > 1 and len(words[-1]) > 1:
        last_word = words[-1]

        # ends with alphanumeric - add a period
        if last_word[-1].isalnum():
            words[-1] += "."

        # ends with a non-alphanumeric character that isn't ? or ! or .
        elif not last_word[-1].isalnum() and last_word[-1] not in ["?", "!", "."]:
            words[-1] = words[-1][:-1] + "."

    return words

