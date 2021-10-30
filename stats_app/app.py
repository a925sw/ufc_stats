from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def home():



@app.route("/search_pages", methods = ["GET", "POST"])
def search_pages():
    
