import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "7P2RT7NFCMIRAUK6"
NEWS_API_KEY = "d7a6452f95114d8cbe46bd9b4e6dcc91"

account_sid = 'AC3fa86fa29e3736a3699149586b4e3150'
auth_token = "2c6369e593122ef318a81c92d67140ac"

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)


data = response.json()["Time Series (Daily)"]
# **** MUY IMPORTANTE DICTIONARY COMPREHENSION ****
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

print(yesterday_closing_price)
bf_yesterday_data = data_list[1]
bf_yesterday_closing_price = float(bf_yesterday_data["4. close"])

print(bf_yesterday_closing_price)
difference = (yesterday_closing_price - bf_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "up"
else:
    up_down = "down"

print(difference)
percentage_difference = round((difference*100)/yesterday_closing_price)
print(f"{percentage_difference}%")


if percentage_difference > 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)

    news_data = news_response.json()["articles"]
    # *** Esto es un slice vvv *** #
    three_articles = news_data[0:3]
    print(three_articles)

article_list = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
# LIST COMPREHENSION ^^^
print(article_list)


client = Client(account_sid, auth_token)
for article in article_list:
    message = client.messages \
                    .create(
                        body=article,
                        from_='+19036485177',
                        to='+5491158870286'
                    )

    print(message.sid)

"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

