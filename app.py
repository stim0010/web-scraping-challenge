from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

#delete if db already exists 
client.drop_database("mars_db")

# Connect to a database. Will create one if not already available.
db = client.mars_db
mars_collection = db.mars_summary


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_data = mars_collection.find_one()

    # Return template and data
    return render_template("index.html", data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def will_scrape():

    mars_data = scrape_mars.scrape()
    db.drop_collection("mars_summary")
    mars_collection = db.mars_summary
    mars_collection.insert(mars_data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)