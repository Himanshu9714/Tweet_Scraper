# Setup

### Create Virtual Environment

Create

```
python -m venv venv
```

Activate

```
venv\Scripts\activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run the script

1. Provide the username for which you want to scrape the tweets
2. Max scroll count defines how many times you want to scroll the page and get the tweets.
3. Run the script<br>
   `python tweet_scraper.py`

### What does the scraper scrapes?

The scraper scrapes the twitter text, datetime on which tweet was published, number of likes on that tweet, and number of times the tweet has been retweeted.
