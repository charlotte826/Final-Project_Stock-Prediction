import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
import TwitterSpecificTweet as tst
import TestNaiveBse as nb
import futureDates
import trainModel
import csv
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


@app.route("/priceprediction")
def priceprediction():
    list_funds_all = []
    path_master_file = os.getcwd() + '/data/ETFSymbols.csv'

    with open(path_master_file) as fp_master_reader:
        read_fund_list = csv.reader(fp_master_reader, delimiter=',')
        for fund in list(read_fund_list):
            for ticker in fund:
                list_funds_all.append(ticker)
    return render_template("prediction.html",option_list = list_funds_all)

# Work from here in the evening

@app.route("/priceopt", methods=['GET', 'POST'])
def priceopt():
    path_img = 'static/images'
    if not os.path.exists(path_img):
        os.mkdir(path_img)
    list_funds_selected = []
    list_funds_all = []
    path_master_file = os.getcwd() + '/data/ETFSymbols.csv'

    with open(path_master_file) as fp_master_reader:
        read_fund_list = csv.reader(fp_master_reader,delimiter=',')
        for fund in list(read_fund_list):
            for ticker in fund:
                list_funds_all.append(ticker)
    
    if request.method == 'POST':
        list_funds_selected = request.form.getlist('option')
        int_projection_days = int(request.form.get('daysForProjection'))
        dict_performance_images = trainModel.TrainTestModel(list_funds_selected, path_img, int_projection_days)
        return render_template('Predictionresult.html', option_list = list_funds_all, item_list = dict_performance_images, sub_img_path = '/' + path_img)


    #return render_template("prediction.html")
@app.route("/sentimentresultsend", methods=["GET", "POST"])

def sentimentresultsend1():
    if request.method == "POST":
        name = request.form["invselect"]
        tst.tweetsOfGivenInvestor(name)
        filename=nb.PlotNaiveBase(name)
        print(filename)
        #filename2 = "C:\Users\suneetha.irigireddy\stockproject\teststock.png"
    return render_template("sentimentresult.html",selectedname=filename)

if __name__== "__main__":
    app.run(debug=True)