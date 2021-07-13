import requests
import smtplib

STOCK_API_KEY = "F61R6QF1L1HVM047"
STOCK_END_POINT = "https://www.alphavantage.co/query"

NEWS_API_KEY = "7686c5b3fade420f9e97c4be16e7fc38"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

MY_EMAIL = "rksv260699@gmail.com"
MY_PASSWORD = "rakesh2606"

#<--------------------------STOCK API------------------------------------->

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY
}

response = requests.get(STOCK_END_POINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
stock_data = [val for key, val in data.items()]

yesterday_data = stock_data[0]["4. close"]
day_before_yesterday_data = stock_data[1]["4. close"]

difference = float(yesterday_data) - float(day_before_yesterday_data)

up_down = ""
if difference > 0:
    up_down = "⬆️"
else:
    up_down = "⬇️"
    difference = -1*difference

diff_percent = "{:.2f}".format(difference*100/float(yesterday_data))


#<--------------------------NEWS API------------------------------------->

news_params = {
    "apiKey" : NEWS_API_KEY,
    "qInTitle": COMPANY_NAME
}

news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
news_data = news_response.json()["articles"]
three_articles = news_data[:3]


#<--------------------------SMTP LIBRARY------------------------------------->

email_data = [f"\n\nHeadline: {article['title']}\n\nDescription: {article['description']}\n for more details click here : {article['url']}\n\n" for article in three_articles]
text = f"Subject:{COMPANY_NAME} stock goes {up_down} by {diff_percent}%\n\n {''.join(email_data)}".encode("utf-8")

if float(diff_percent) >= 5:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="rakeshbudde06@gmail.com",
            msg=text
        )
