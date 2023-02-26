from flask import Flask

import requests

app = Flask(__name__)

@app.route('/')
def get_prices():
    try:
        # Fetching the latest prices of all available cryptocurrencies on Binance
        response = requests.get('https://api.binance.com/api/v3/ticker/price')
        prices = response.json()
        return prices
    except requests.exceptions.RequestException as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
