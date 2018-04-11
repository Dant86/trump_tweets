from dotenv import load_dotenv
import os
import twitter
from wordfreq import simple_tokenize
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

load_dotenv()
cKey = os.environ.get("CONSUMER_KEY")
cSec = os.environ.get("CONSUMER_SECRET")
aKey = os.environ.get("ACCESS_TOKEN_KEY")
aSec = os.environ.get("ACCESS_TOKEN_SECRET")

api = twitter.Api(consumer_key=cKey,
                  consumer_secret=cSec,
                  access_token_key=aKey,
                  access_token_secret=aSec,
                  tweet_mode="extended")

# Get Trump's past tweets
new_tweets = api.GetUserTimeline(screen_name="realDonaldTrump", count=200)
all_tweets = []
all_tweets.extend(new_tweets)
while len(new_tweets) != 0:
    oldest_id = all_tweets[-1].id - 1
    new_tweets = api.GetUserTimeline(screen_name="realDonaldTrump",
                                     count=200, max_id=oldest_id)
    all_tweets.extend(new_tweets)
    print("{} tweets retrieved so far...".format(len(all_tweets)))
trump_tweets = [tweet.full_text for tweet in all_tweets]

# Now, let's take a look at Trump's 10 most recent tweets just for kicks
print(trump_tweets[:10])

# Let's take a look at a few of Trump's most commonly-used words
tokenized_tweets = [simple_tokenize(tweet) for tweet in trump_tweets]
counts = {}
for tokenized in tokenized_tweets:
    for word in tokenized:
        if word not in stopwords.words("english"):
        if word != "https" and word != "t.co" and word != "rt":
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1
sorted_counts = sorted(counts, key=counts.get, reverse=True)
top_20_keys = sorted_counts[:20]
top_20_values = [counts[key] for key in top_20_keys]
plt.style.use("ggplot")
plt.bar(top_20_keys, top_20_values, color="blue")
plt.ylabel("Frequencies")
plt.title("Trump's most commonly-used words on Twitter")
plt.show()