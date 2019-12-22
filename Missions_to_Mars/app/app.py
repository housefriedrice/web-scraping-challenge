import pymongo 
from flask import Flask, render_template
from scrape_mars import scrape


client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.MarsDB


app = Flask(__name__)

@app.route("/")
def displaydata():
    data = list(db.posts.find())[-1]
    return render_template("index.html", data=data)

@app.route("/scrape")
def flaskscrape():
    scrapings = scrape()
    db.posts.insert_one(scrapings)
    return "Scraping Complete!"


if __name__ == "__main__":
    app.run(debug=True)