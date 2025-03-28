import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
import ssl

# SSL Certificate fix
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download required NLTK data
nltk.download('vader_lexicon')

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    
    compound_score = sentiment_scores['compound']
    
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'

def analyze_product_comments(comments):
    results = {
        'positive': [],
        'negative': [],
        'neutral': []
    }
    
    for comment in comments:
        sentiment = analyze_sentiment(comment)
        results[sentiment].append(comment)
    
    return results

# Example usage
if __name__ == "__main__":
    # Sample product comments
    product_comments = [
        "This product is amazing! Really satisfied with the quality.",
        "Worst purchase ever, completely disappointed.",
        "The product is okay, nothing special.",
        "Excellent customer service and fast delivery!",
        "The product broke after two days.",
        "It meets my expectations.",
        "Absolutely love this product, worth every penny!",
        "Not sure if I like it or not.",
    ]
    
    # Analyze comments
    categorized_comments = analyze_product_comments(product_comments)
    
    # Print results
    print("\nPositive Comments:")
    for comment in categorized_comments['positive']:
        print(f"- {comment}")
        
    print("\nNegative Comments:")
    for comment in categorized_comments['negative']:
        print(f"- {comment}")
        
    print("\nNeutral Comments:")
    for comment in categorized_comments['neutral']:
        print(f"- {comment}")

    # Create a DataFrame for better visualization
    df = pd.DataFrame({
        'Category': ['Positive', 'Negative', 'Neutral'],
        'Count': [
            len(categorized_comments['positive']),
            len(categorized_comments['negative']),
            len(categorized_comments['neutral'])
        ]
    })
    
    print("\nSummary:")
    print(df)