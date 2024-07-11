import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download the VADER lexicon if not already downloaded


#nltk.download('vader_lexicon')


def analyze_sentiment(text):
    # Initialize VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    # Analyze sentiment
    sentiment_score = sia.polarity_scores(text)
    # Determine sentiment label
    if sentiment_score['compound'] >= 0.05:
        sentiment = 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    #return sentiment, sentiment_score
    return sentiment

if __name__ == "__main__":
    # Example text for sentiment analysis
    text = "I love this movie. It's fantastic!"
    
    # Analyze sentiment
    #sentiment, sentiment_score = analyze_sentiment(text)
    sentiment= analyze_sentiment(text)
    
    # Print results
    print("Text:", text)
    print("Sentiment:", sentiment)
    #print("Sentiment Scores:", sentiment_score)
