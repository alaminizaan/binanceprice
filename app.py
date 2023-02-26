from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def binance_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    querystring = {"symbol":""}
    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        prices = response.json()
        return render_template('binance_price.html', prices=prices)
    else:
        return "Error getting prices from Binance API"

if __name__ == '__main__':
    app.run(debug=True)
