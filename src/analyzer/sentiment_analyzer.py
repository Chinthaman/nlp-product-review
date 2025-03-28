from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class ProductSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_review(self, review):
        """Single review analysis - used by both apps"""
        scores = self.analyzer.polarity_scores(review)
        sentiment = self._get_sentiment_label(scores['compound'])
        return {
            'text': review,
            'scores': scores,
            'sentiment': sentiment
        }

    def analyze_comments(self, comments):
        """Batch analysis - used by both apps"""
        results = {
            'positive': [],
            'neutral': [],
            'negative': [],
            'average_scores': {'pos': 0, 'neu': 0, 'neg': 0, 'compound': 0}
        }
        
        for comment in comments:
            analysis = self.analyze_review(comment)
            results[analysis['sentiment']].append(comment)
            
            # Update average scores
            for key in analysis['scores']:
                results['average_scores'][key] += analysis['scores'][key]
        
        # Calculate final averages
        num_comments = len(comments)
        if num_comments > 0:
            for key in results['average_scores']:
                results['average_scores'][key] /= num_comments
        
        return results

    def _get_sentiment_label(self, compound_score):
        """Determine sentiment label based on compound score"""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        return 'neutral'

    def generate_customer_conclusion(self, results):
        """Generate detailed conclusion for customers"""
        avg_scores = results['average_scores']
        pos_count = len(results['positive'])
        neg_count = len(results['negative'])
        total_reviews = len(results['positive']) + len(results['negative']) + len(results['neutral'])
        
        # Calculate percentages
        pos_percentage = (pos_count / total_reviews) * 100
        neg_percentage = (neg_count / total_reviews) * 100
        
        # Generate main conclusion
        if avg_scores['compound'] >= 0.05:
            main_conclusion = (
                "✨ Product Highlights:\n"
                f"• {int(pos_percentage)}% of customers had a positive experience\n"
                "• Strong points: Quality and customer satisfaction\n"
                "• Recommended for: Users looking for reliable products"
            )
        elif avg_scores['compound'] <= -0.05:
            main_conclusion = (
                "⚠️ Consider Before Buying:\n"
                f"• {int(neg_percentage)}% of customers reported concerns\n"
                "• Common issues: Product durability and expectations\n"
                "• Suggestion: Compare with similar products"
            )
        else:
            main_conclusion = (
                "📝 Balanced Feedback:\n"
                "• Product meets basic expectations\n"
                "• Mixed reviews on features and quality\n"
                "• Consider your specific needs before purchase"
            )
        
        return main_conclusion