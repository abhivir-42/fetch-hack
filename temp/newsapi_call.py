#pip install newsapi-python
from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key="94b2d38f6b104eafa2f041bc323ed03c")
crypto_news = newsapi.get_everything(q="crypto OR cryptocurrency OR bitcoin OR ethereum OR financial market OR crypto exchange OR bullish OR bearish OR recession OR FOMC", language="en")

print(crypto_news)
