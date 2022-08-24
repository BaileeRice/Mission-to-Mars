# Dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask:
app = Flask(__name__)

# tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app) # This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app"

# define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# set up our scraping route, This route will be the "button" of the web application
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# update the database using .update_one()
# mars.update_one(query_parameter, {"$set": data}, options)

# tell flask to run
if __name__ == "__main__":
   app.run()