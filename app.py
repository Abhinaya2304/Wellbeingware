from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3
from datetime import datetime

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = request.form['mood']
        journal = request.form['journal']
        result = analyzer.polarity_scores(journal)
        sentiment = result['compound']

        # Motivational quotes by mood
        quotes = {
            "Happy": "Keep spreading the joy!",
            "Sad": "You're not alone. Better days are coming.",
            "Angry": "Stay calm. You're stronger than anger.",
            "Anxious": "Breathe. You're doing better than you think.",
            "Neutral": "Every day is a new chance to grow."
        }

        quote = quotes.get(mood, "")

        # Save to database
        conn = sqlite3.connect('journal.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                mood TEXT,
                journal TEXT,
                sentiment REAL,
                quote TEXT
            )
        ''')
        c.execute('INSERT INTO entries (date, mood, journal, sentiment, quote) VALUES (?, ?, ?, ?, ?)',
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood, journal, sentiment, quote))
        conn.commit()
        conn.close()

        return render_template('index.html', sentiment=sentiment, quote=quote)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)