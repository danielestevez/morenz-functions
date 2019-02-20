import json
import logging
import os

from azure.functions import HttpRequest, HttpResponse
from twython import Twython


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger twittercode-daily started')
    code = get_daily_code()
    logging.info(f"Today's code was {code}  !")
    return HttpResponse(code, status_code=200, mimetype="application/json")


def get_daily_code():
    app_key = os.environ['twitter_app_key']
    app_secret = os.environ['twitter_app_secret']
    twitter = Twython(app_key, app_secret)

    code_found_str = twitter.search(q='Le code Club 1909 du jour. / Today\'s Club 1909 code', result_type='recent',
                                    count=1)
    logging.info('Twitter search OK returned = %s', code_found_str)
    tweet_text = code_found_str.get('statuses').pop().get('text')
    code = tweet_text[tweet_text.find("Today's Club 1909 code. \n") + 25: tweet_text.find("http") - 1]
    logging.info("Today's code is %s", code)
    # RT @CanadiensMTL: Le code Club 1909 du jour. / Today's Club 1909 code. \nXXXX

    return json.dumps({"code": code})
