from textblob import TextBlob


def sentiment(text):
    return TextBlob(text).sentiment.polarity


def avg_sentiment(listIn):
    sumIn = 0
    for text in listIn:
        sumIn += sentiment(text)
    return sumIn / len(listIn)
