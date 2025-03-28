import streamlit as st
import pandas as pd
import plotly.express as px
from src.analyzer.sentiment_analyzer import ProductSentimentAnalyzer
import json  # Add this import

def load_file_content(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'json':
            data = json.load(uploaded_file)
            return data.get('comments', [])
            
        elif file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            # Assuming the reviews are in a column named 'review' or the first column
            review_column = df.columns[0]
            return df[review_column].tolist()
            
        elif file_extension == 'txt':
            content = uploaded_file.read().decode('utf-8')
            # Split by new lines and remove empty lines
            return [line.strip() for line in content.split('\n') if line.strip()]
            
        else:
            st.error("Unsupported file format. Please upload JSON, CSV, or TXT file.")
            return []
    return []

def main():
    st.set_page_config(page_title="Product Review Sentiment Analyzer", page_icon="🎯")
    
    st.title("Product Review Sentiment Analyzer 🎯")
    
    # Initialize ProductSentimentAnalyzer instead of direct VADER
    analyzer = ProductSentimentAnalyzer()
    # Uses both analyze_review() for single reviews
    # and analyze_comments() for file uploads
    
    # Add file upload option with proper label
    st.write("Choose your input method:")
    input_method = st.radio(
        label="Input Method",
        options=["Enter Text", "Upload File"],
        label_visibility="collapsed"
    )
    
    if input_method == "Enter Text":
        col_input, col_graph = st.columns([3, 2])
        
        with col_input:
            user_input = st.text_area("Enter your product review:", height=100)
            
            if st.button("Analyze Single Review"):
                if user_input:
                    # Use ProductSentimentAnalyzer's method
                    result = analyzer.analyze_review(user_input)
                    scores = result['scores']
                    compound_score = scores['compound']
                    
                    # Convert scores to clean percentages
                    pos_percent = int(scores['pos'] * 100)
                    neu_percent = int(scores['neu'] * 100)
                    neg_percent = int(scores['neg'] * 100)
                    show_graph = True
                    
                    # Display scores as clean percentages
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Positive", f"{pos_percent}%")
                    with col2:
                        st.metric("Neutral", f"{neu_percent}%")
                    with col3:
                        st.metric("Negative", f"{neg_percent}%")
                    
                    # Show total
                    total = pos_percent + neu_percent + neg_percent
                    st.write(f"Total: {total}%")
                    
                    # Final conclusion with loading bar
                    st.write("---")
                    st.write("Sentiment Score:")
                    
                    # Create a centered progress bar with labels
                    col1, col2, col3 = st.columns([1,3,1])
                    with col1:
                        st.write("-1")
                    with col2:
                        st.progress((compound_score + 1) / 2)
                    with col3:
                        st.write("+1")
                    
                    # Show final score and conclusion
                    st.write(f"Score: {compound_score:.2f}")
                    if compound_score >= 0.05:
                        st.success("""
                        Positive Review 😊
                        • Product meets quality standards
                        • Good customer satisfaction
                        """)
                    elif compound_score <= -0.05:
                        st.error("Negative Review 😔")
                        st.warning("""
                        Note: Our team has been notified about the concerns.
                        • Feedback sent to product team
                        • Quality improvement process initiated
                        • Customer service will follow up
                        """)
                    else:
                        st.info("""
                        Neutral Review 😐
                        • Basic expectations met
                        • Room for improvement noted
                        """)
                    
                    # Add pie chart in the graph column
                    with col_graph:
                        df = pd.DataFrame({
                            'Sentiment': ['Positive', 'Neutral', 'Negative'],
                            'Score': [scores['pos'], scores['neu'], scores['neg']]
                        })
                        
                        fig = px.pie(df, values='Score', names='Sentiment',
                                    color_discrete_sequence=['#00CC96', '#636EFA', '#EF553B'],
                                    title='Sentiment Distribution')
                        fig.update_layout(margin=dict(t=40, b=40))
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Continue with existing code for progress bar and conclusions...
    else:
        # File upload and batch analysis
        uploaded_file = st.file_uploader("Upload your reviews file", type=['json', 'csv', 'txt'])
        
        if uploaded_file and st.button("Analyze File"):
            reviews = load_file_content(uploaded_file)
            
            if reviews:
                # Use ProductSentimentAnalyzer's batch analysis
                results = analyzer.analyze_comments(reviews)
                avg_scores = results['average_scores']
                
                st.write(f"Analyzing {len(reviews)} reviews...")
                
                # Display results similar to single review
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Positive", f"{int(avg_scores['pos']*100)}%")
                with col2:
                    st.metric("Neutral", f"{int(avg_scores['neu']*100)}%")
                with col3:
                    st.metric("Negative", f"{int(avg_scores['neg']*100)}%")
                
                # Show total
                total = int(avg_scores['pos']*100) + int(avg_scores['neu']*100) + int(avg_scores['neg']*100)
                st.write(f"Total: {total}%")
                
                # Final conclusion with loading bar
                st.write("---")
                st.write("Overall Sentiment Score:")
                
                # Create a centered progress bar with labels
                col1, col2, col3 = st.columns([1,3,1])
                with col1:
                    st.write("-1")
                with col2:
                    st.progress((avg_scores['compound'] + 1) / 2)
                with col3:
                    st.write("+1")
                
                # Show final score and conclusion
                st.write(f"Score: {avg_scores['compound']:.2f}")
                if avg_scores['compound'] >= 0.05:
                    st.success("Overall: Positive Reviews 😊")
                elif avg_scores['compound'] <= -0.05:
                    st.error("Overall: Negative Reviews 😔")
                    st.warning("Note: Our team has been notified about the concerns, and we're working on improvements.")
                else:
                    st.info("Overall: Neutral Reviews 😐")
                
                # Create pie chart
                col_stats, col_chart = st.columns([1, 1])
                
                with col_stats:
                    st.subheader("Review Breakdown")
                    st.write(f"✅ Positive Reviews: {len(results['positive'])}")
                    st.write(f"➖ Neutral Reviews: {len(results['neutral'])}")
                    st.write(f"❌ Negative Reviews: {len(results['negative'])}")
                
                with col_chart:
                    df = pd.DataFrame({
                        'Sentiment': ['Positive', 'Neutral', 'Negative'],
                        'Score': [avg_scores['pos'], avg_scores['neu'], avg_scores['neg']]
                    })
                    
                    fig = px.pie(df, values='Score', names='Sentiment',
                                color_discrete_sequence=['#00CC96', '#636EFA', '#EF553B'],
                                title='Sentiment Distribution')
                    fig.update_layout(margin=dict(t=40, b=40))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Add conclusion section
                st.write("---")
                st.subheader("🎯 Analysis Summary")
                
                # Calculate percentages
                total_reviews = len(reviews)
                pos_count = len(results['positive'])
                neg_count = len(results['negative'])
                neu_count = len(results['neutral'])
                
                # Display conclusion based on overall sentiment
                if avg_scores['compound'] >= 0.05:
                    st.success(f"""
                    ✨ Product Analysis:
                    • {int((pos_count/total_reviews)*100)}% customers reported positive experiences
                    • Strong points: Product quality and satisfaction
                    • Verdict: Recommended product with good customer feedback
                    
                    💡 Key Insights:
                    • Product shows consistent quality and reliability
                    • Good value for money investment
                    • High customer satisfaction rate
                    """)
                elif avg_scores['compound'] <= -0.05:
                    st.error(f"""
                    ⚠️ Product Analysis:
                    • {int((neg_count/total_reviews)*100)}% customers reported issues
                    • Common concerns: Product reliability and expectations
                    • Verdict: Product improvement process initiated
                    
                    💡 Action Taken:
                    • Seller has been notified of customer concerns
                    • Quality improvement process in progress
                    • Enhanced quality control measures being implemented
                    • Customer feedback is being addressed
                    """)
                else:
                    st.info(f"""
                    📝 Product Analysis:
                    • Mixed feedback from customers
                    • Product meets basic expectations
                    • Verdict: Research specific features you need before purchase
                    
                    💡 Enhancement Suggestions:
                    • Consider adding unique features
                    • Focus on consistency in performance
                    • Improve overall user experience
                    """)

if __name__ == "__main__":
    main()