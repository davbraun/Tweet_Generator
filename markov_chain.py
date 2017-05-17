import random

def get_dict(longtweet):
    #Takes list of tweets and returns a random tweet using a markov chain algorithm

    #First lets build out dictionaries!

    #concatnating all the tweets into one long string

    #Building dictionary#1
    #This dictionary will contain words as keys and words that may follow it as values
    #This dictionary should contain multiples if necessary

    longtweet_list = longtweet
	
    # $ means words at the beginning of a sentence
    dict1 = {"$": [longtweet_list[0]], longtweet_list[0]: []}
                 
    for i in range(1, len(longtweet_list)):
        # add word as a key to dictionary#1 initializes it with an empty list
        if longtweet_list[i] not in dict1:
            dict1[longtweet_list[i]] = []

        # if not first word, add this word as a value to the word before's key
        word_before_key = longtweet_list[i-1]
            
        if word_before_key[-1] in ["?", "!", "."]:
            word_before_value = dict1.get("$")
        else:
            word_before_value = dict1.get(word_before_key)

        word_before_value.append(longtweet_list[i])

    #tweet = gen_markov_tweet(dict1)
    return dict1

def gen_markov_tweet(dict1):
    #Takes the dictionary formed from the build_markov_model function

    working = True
    
    while working:
        #First lets pick a random word to start
        key_word = random.choice(dict1['$'])

        #Add this word to the markov-chain tweet we will later return
        markov_tweet = [key_word]

        # in words
        maximum_tweet_size = 25

        #Now lets move on to the following words, we will end our fucntion when a word with punctuation is picked
        finished_tweet = False
        
        while not finished_tweet:
            #Let's make sure our tweet isn't getting too long! Max tweet length is 140 characters
            if len(markov_tweet) > maximum_tweet_size:
                markov_tweet = []
                finished_tweet = True
                break

            last_word = markov_tweet[-1]
            next_word = random.choice(list(dict1[last_word]))
            
            #If word has punctuation and there are at least 3 words in the tweet, end the tweet
            if next_word[-1] in ["?", "!", "."]:
                markov_tweet.append(next_word)
                finished_tweet = True
                break
            else:
                markov_tweet.append(next_word)

        if markov_tweet != []:
            working = False

    # capitalize
    markov_tweet[0] = markov_tweet[0][0].upper() + markov_tweet[0][1:]
    final = " ".join(markov_tweet)
    return final