from datetime import datetime
import yfinance as yf
from flask import Flask
from flask import render_template
from flask import request



app = Flask(__name__)

@app.route('/',  methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        now = datetime.now()

        symbol = request.form.get("symbol")
    
        companyInfo = yf.Ticker(symbol)
        negativeValueChange = False
        negativePercentageChange = False

        if companyInfo.history(period="max").empty is False:

            companyName=companyInfo.info['longName']
            twoDaysData = round(companyInfo.history(period='2d'),2)
            yesterdayPrice=twoDaysData['Close'][0]
            todaysPrice=twoDaysData['Close'][1]
            valueChange=round(todaysPrice-yesterdayPrice,2)
            if(valueChange < 0):
                negativeValueChange = True;
            percentChange=round((valueChange/yesterdayPrice)*100,2)
            if(percentChange < 0):
                negativePercentageChange = True;
           
            if(not negativeValueChange):
                valueChange = '+ '+str(valueChange)
            if(not negativePercentageChange):
                percentChange = '+ '+str(percentChange)

            tempData = {"now": now, "companyName": companyName, 
                 "twoDaysData":twoDaysData['Close'][1],"valueChange":valueChange,"percentChange":percentChange, "error" :""}
            return render_template("index.html", **tempData)
             
        else:
            tempData = {"error":"Wrong Symbol!"}
            return render_template("index.html", **tempData)


if __name__ == '__main__':
    #app = create_app()

    app.run(debug=False, host='0.0.0.0', port=8080)
    # main()
