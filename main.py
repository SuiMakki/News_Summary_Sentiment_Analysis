import tkinter as tk
from newspaper import Article
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import re

nltk.download('stopwords')


def analyze_sentiment(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]

    # Join the filtered words back into a string
    filtered_text = ' '.join(filtered_words)

    # Perform sentiment analysis
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(filtered_text)

    # Classify sentiment based on compound score
    compound_score = sentiment_score['compound']
    if compound_score >= 0.05:
        return 'positive'
    elif compound_score <= -0.05:
        return 'negative'
    else:
        return 'neutral'


def extract_author(text):
    # Define regular expression patterns to capture author information
    author_patterns = [
        r'By: (.+)',          # Pattern: By: Author Name
        r'By (.+)',           # Pattern: By Author Name
        r'Author: (.+)',      # Pattern: Author: Author Name
        r'Writer: (.+)',      # Pattern: Writer: Author Name
    ]

    # Try to match each pattern to extract the author
    for pattern in author_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    # Return None if no author information is found
    return None


def summarize():
    url = utext.get('1.0', "end").strip()

    # Initialize a new Article object
    article = Article(url)

    # Download the article content
    article.download()

    # Parse the article
    article.parse()

    # Perform natural language processing (optional)
    article.nlp()

    # Perform sentiment analysis
    sentiment = analyze_sentiment(article.text)

    # Print article details
    # print(f'Title: {article.title}')
    # print(f'Authors: {article.authors}')  # this line for debugging

    # Print article details
    # print(f'Title: {article.title}')
    # print(f'Author: {article.authors}')
    # print(f'Publication Date: {article.publish_date}')
    # print(f'Summary: {article.summary}')

    title.config(state='normal')
    author.config(state='normal')
    summary.config(state='normal')
    publication.config(state='normal')
    sentiment_field.config(state='normal')

    title.delete(1.0, "end")
    title.insert(1.0, article.title)

    # Handle author information
    author_text = extract_author(article.text) or "Author information not available"
    author.insert(1.0, author_text)

    summary.delete(1.0, "end")
    summary.insert(1.0, article.summary)

    publication_date = str(article.publish_date) if article.publish_date else "Publication date not available"
    publication.delete(1.0, "end")
    publication.insert(1.0, publication_date)

    sentiment_field.delete('1.0', "end")
    sentiment_field.insert('1.0', f'Sentiment: {sentiment}')

    title.config(state='disabled')
    author.config(state='disabled')
    summary.config(state='disabled')
    publication.config(state='disabled')
    sentiment_field.config(state='disabled')


# Rest of your GUI code...



# Rest of your GUI code...


root = tk.Tk()
root.title("News Summarizer")
root.geometry('1200x600')

tlabel = tk.Label(root, text="Title")
tlabel.pack()

title = tk.Text(root, height=1, width=140)
title.config(state='disabled', bg='#dddddd')
title.pack()

alabel = tk.Label(root, text="Author")
alabel.pack()

author = tk.Text(root, height=1, width=140)
author.config(state='disabled', bg='#dddddd')
author.pack()

plabel = tk.Label(root, text="Publication Date")
plabel.pack()

publication = tk.Text(root, height=1, width=140)
publication.config(state='disabled', bg='#dddddd')
publication.pack()

slabel = tk.Label(root, text="Summary")
slabel.pack()

summary = tk.Text(root, height=20, width=140)
summary.config(state='disabled', bg='#dddddd')
summary.pack()

selabel = tk.Label(root, text="Sentiment")
selabel.pack()

sentiment_field = tk.Text(root, height=1, width=140)
sentiment_field.config(state='disabled', bg='#dddddd')
sentiment_field.pack()

ulabel = tk.Label(root, text="URL")
ulabel.pack()

utext = tk.Text(root, height=1, width=140)
utext.pack()

btn = tk.Button(root, text="Summarizer", command=summarize)
btn.pack()

root.mainloop()
