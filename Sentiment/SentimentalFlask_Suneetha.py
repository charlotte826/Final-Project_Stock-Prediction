import os
import futureDates
import trainModel
import futureProjection
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

@app.route("/priceprediction")
def priceprediction():
    return render_template("prediction.html")

@app.route("/priceopt")
def priceopt():
    return render_template("prediction.html")

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

@app.route("/predictprice", methods=["GET", "POST"])
def predictprice():
    if request.method == "POST":
        list_etf = request.form["etf_fund"]
        daysForProjection = request.form["daysForProjection"]
        #dict_stock = trainModel.TrainTestModel(stock_name)
        dict_fund_model = {}
        dict_r2 = {}
        for etf in list_etf:
            model_etf = trainModel.TrainTestModel(etf)
            dict_r2[etf] = model_etf['r2']
            dict_fund_model[etf] = model_etf
        #dict_future_projection = {}
        #for etf_iterator in range(0,len(list_etf)):
        #fund_lr_model = dict_fund_model[list_etf[etf_iterator]]
        
        dict_fund_progress_graphs = futureProjection.fundFutureProjection(dict_fund_model,list_etf, int(daysForProjection))
        
        #dict_fund_model[stock_name] = trainModel.TrainTestModel(stock_name)
        #daysForProjection = 500
        #dict_future_projection = futureProjection.fundFutureProjection(dict_fund_model,stock_name,int(daysForProjection))
        #(dict_trained_stock_model, etf_fund, future_proj_days):
        length = len(list_etf)
    return render_template("prediction.html", dict_fund_progress_graphs = dict_fund_progress_graphs, list_etf = list_etf, length = length)
if __name__== "__main__":
    app.run(debug=True)