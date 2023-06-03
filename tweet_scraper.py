from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

import pandas as pd

# Static url
TWEET_URL = r"https://twitter.com/"

# Static classes
TWEETER_TEXT_CLASS = "css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"
TWEETER_DATES_CLASS = "css-4rbku5 css-18t94o4 css-901oao r-14j79pv r-1loqt21 r-xoduu5 r-1q142lx r-1w6e6rj r-37j5jr r-a023e6 r-16dba41 r-9aw3ui r-rjixqe r-bcqeeo r-3s2u2q r-qvutc0"
TWEETER_STATS_CLASS = "css-1dbjc4n r-1ta3fxp r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws"


class TweetScraper:
    def __init__(self, username_to_scrape, max_scroll_count=10) -> None:
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.url = TWEET_URL + username_to_scrape
        self.data = []
        self.max_scroll_count = max_scroll_count

    def scroll_page(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        html_content = self.driver.page_source
        return html_content

    def extract_tweet_texts(self, soup):
        tweet_texts_elements = soup.find_all(class_=TWEETER_TEXT_CLASS)
        return tweet_texts_elements

    def extract_tweet_dates(self, soup):
        tweet_dates_elements = soup.find_all(class_=TWEETER_DATES_CLASS)
        return tweet_dates_elements

    def extract_tweet_stats(self, soup):
        tweet_stats_elements = soup.find_all(class_=TWEETER_STATS_CLASS)
        return tweet_stats_elements

    def get_like_retweet_reply_from_tweet_stats(self, stats):
        like, retweet, reply = None, None, None
        tweet_stats_data = stats.get("aria-label")
        if tweet_stats_data is not None:
            tweet_stats_data = tweet_stats_data.lower()
            stats_list = tweet_stats_data.split(",")
            for stat in stats_list:
                strip_data = stat.strip().split(" ")[0]
                if "like" in stat:
                    like = strip_data
                elif "retweet" in stat:
                    retweet = strip_data
                elif "repl" in stat:
                    reply = strip_data

        return like, retweet, reply

    def extract_tweet_details(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        tweet_texts = self.extract_tweet_texts(soup)
        tweet_dates = self.extract_tweet_dates(soup)
        tweet_stats = self.extract_tweet_stats(soup)

        for text, date, stats in zip(tweet_texts, tweet_dates, tweet_stats):
            tweet_raw = {
                "tweet_text": None,
                "tweet_date": None,
                "tweet_like": None,
                "tweet_retweet": None,
            }
            tweet_raw["tweet_text"] = text.get_text()
            date_time_tag = date.find("time")
            tweet_raw["tweet_date"] = date_time_tag.get("datetime")

            like, retweet, reply = self.get_like_retweet_reply_from_tweet_stats(stats)
            tweet_raw["tweet_like"] = like
            tweet_raw["tweet_retweet"] = retweet
            if not tweet_raw in self.data:
                self.data.append(tweet_raw)

        print(f"Added data to the list...\n")

    def scrape_twitter(self):
        print(f"GETTING TWEET URL: {self.url}...")
        self.driver.get(self.url)
        print("Entered into url successfully!\n\n")
        for idx in range(self.max_scroll_count):
            print(f"Scrolling page index: {idx}...")
            html_content = self.scroll_page()

            print(f"Get tweet text, date, and stats data for index {idx}..")
            self.extract_tweet_details(html_content)

            print(f"Starting for next index {idx+1} after 1 seconds...")
            time.sleep(1)

    def create_csv_of_scraped_data(self, csv_file_name="data.csv"):
        print("Creating dataframe")
        df = pd.DataFrame(self.data)

        print("Storing to CSV...")
        df.to_csv(csv_file_name)

        print("Scraped data stored to CSV successfully!")

    def scrape_twitter_and_store_data_to_csv(self, csv_file_name="data.csv"):
        self.scrape_twitter()
        self.create_csv_of_scraped_data(csv_file_name)


# Username for which tweet stats needs to be scrape
username = input()
tweet_scrape = TweetScraper(username, 20)
tweet_scrape.scrape_twitter_and_store_data_to_csv("new.csv")
