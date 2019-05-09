import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import TwitterSpecificTweet as tst
import TestNaiveBse as nb
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sentimentsend")
def sentimentsend():
    return render_template("sentiment.html")

@app.route("/sentimentopt")

def sentimentopt():

    return render_template("sentiment.html")
@app.route("/sentimentresultsend", methods=["GET", "POST"])
def sentimentresultsend():
    if request.method == "POST":
        name = request.form["invselect"]
        tst.tweetsOfGivenInvestor(name)
        filename=nb.PlotNaiveBase(name)
        print(filename)
        #filename2 = "C:\Users\suneetha.irigireddy\stockproject\teststock.png"
    return render_template("sentimentresult.html",selectedname=filename)
if __name__== "__main__":
    app.run(debug=True)