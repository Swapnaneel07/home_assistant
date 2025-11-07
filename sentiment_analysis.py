# sentiment_analysis.py
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the analyzer
sid = SentimentIntensityAnalyzer()

def get_sentiment(text):
    """
    Analyzes sentiment using your custom thresholds.
    """
    scores = sid.polarity_scores(text)
    compound = scores['compound']
    
    # Using thresholds from your main.py
    if compound > 0.3:
        return "Happy"
    elif compound < -0.1:
        return "Stressed"
    else:
        return "Neutral"