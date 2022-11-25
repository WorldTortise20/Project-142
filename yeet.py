from flask import Flask, jsonify, request
import csv

from demographic import output
from content import get_recommendations


all_articles = []

with open('articles.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_articles = []
disliked_articles = []

app = Flask(__name__)

@app.route("/get-articles")
def get_article():
    art_data = {
        'url': all_articles[0][11],
        'title': all_articles[0][12],
        'text': all_articles[0][13],
        'lang': all_articles[0][14],
        'total_events': all_articles[0][15],
    }
    return jsonify({
        "data": art_data,
        "status": "success"
    })

@app.route("/liked-article", methods=["POST"])
def liked_article():
    article = all_articles[0]
    liked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-movie", methods=["POST"])
def unliked_movie():
    article = all_articles[0]
    disliked_articles.append(article)
    all_articles.pop(0)
    return jsonify({
        "status": "success"
    }), 201

@app.route('/popular_articles')
def popular_articles():
    article_data = []
    for article in output:
        deez = {
            'url': article[0],
            'title': article[1],
            'text': article[2],
            'lang': article[3],
            'total_events': article[4],
        }
        article_data.append(deez)
    return jsonify({
        "data": article_data,
        "status": "Ladies and Gentlemen, we got em"
    }),200

@app.route('/recommended_articles')
def recom_articles():
    all_recom = []
    for liked_art in liked_articles:
        output = get_recommendations(liked_art[4])
        for intel in output:
            all_recom.append(intel)
    import itertools
    all_recom.sort()
    all_recom = list(all_recom for all_recom in itertools.groupby(all_recom))
    article_intel = []
    for recommended in all_recom:
        oklahoma = {
            "url": recommended[0],
            "title": recommended[1],
            "text": recommended[2],
            "lang": recommended[3],
            "total_events": recommended[4]
        }
        article_intel.append(oklahoma)
    return jsonify({
        "data": article_intel,
        "status": "success"
    }), 200

if __name__ == "__main__":
  app.run()