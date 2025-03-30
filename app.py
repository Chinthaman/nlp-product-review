import pandas as pd
import json
from src.utils.ssl_handler import configure_ssl
from src.analyzer.sentiment_analyzer import ProductSentimentAnalyzer
import streamlit as st
# Import other necessary modules
from utils.customization import apply_customizations

def load_comments(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['comments']

def main():
    analyzer = ProductSentimentAnalyzer()
    # Uses analyze_comments() for batch processing
    # Load product comments from JSON file
    product_comments = load_comments('data/product_comments.json')
    
    # Analyze comments
    categorized_comments = analyzer.analyze_comments(product_comments)
    
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

    # Apply customizations first
    custom_settings = apply_customizations()
    
    # If customizations were applied, use them
    if custom_settings:
        st.title(custom_settings.get("app_title", "NLP Sentiment Analyzer"))
        st.markdown(custom_settings.get("welcome_message", "Welcome to the NLP Sentiment Analyzer!"))
    else:
        # Default title and welcome message if no customizations
        st.title("NLP Sentiment Analyzer")
        st.markdown("Welcome to the NLP Sentiment Analyzer!")
    
    # Rest of your application code
    # ...
    
    # Use footer from customizations if available
    if custom_settings and "footer_text" in custom_settings:
        st.markdown(f"<div style='text-align: center; margin-top: 30px;'>{custom_settings['footer_text']}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()