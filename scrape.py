# importing the dependencies
from ntscraper import Nitter
import time
import datetime
import dateparser

# Define my list of accounts
xStockAccounts = ["Mr_Derivatives","warrior_0719","ChartingProdigy","allstarcharts","yuriymatso","TriggerTrades","AdamMancini4","CordovaTrades","Barchart","RoyLMattox"]

# using ntscraper to create a scraper object
scraper = Nitter(log_level=1, skip_instance_check=False)

# creating a template to get the data I need
data = {
  'text': [],
  'date': []
}

# define a function that takes a list of accounts, a term to look for and a period of time in minutes
def getalltweets(accounts,term,period):
  # initialize my counter
  count=0

  # I get the latest tweets from every account
  for account in accounts:
    tweets = scraper.get_tweets(account,mode='user',number=10)
    for tweet in tweets['tweets']:
      # discard pinned tweets (they usually are a part of the result because they are at the top of the page)
      if tweet['is-pinned'] == False:
        # compare the time the tweet was created at to the period passed to the function
        a = datetime.datetime.now(datetime.UTC)
        b = dateparser.parse(tweet['date'])
        c = a-b
        minutes = c.total_seconds() / 60
        # if the person did tweet it during the time period then add it to my dataset
        if minutes < period:
          data['text'].append(tweet['text'])
          data['date'].append(tweet['date'])
    # time so Nitter doesn't block the request
    time.sleep(15)
  # if the term is in the tweet then it adds it to the counter
  for tweet in data['text']:
    if tweet.find(term) != -1:
      number_of_times = tweet.count(term)
      count += number_of_times
  # output
  print(term,'was mentioned',count,'times','in the last',period,'minutes')
      

getalltweets(xStockAccounts,'$SPX',30)
