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