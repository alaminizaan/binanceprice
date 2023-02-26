from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Fetching the latest prices of all available cryptocurrencies on Binance
    response = requests.get('https://api.binance.com/api/v3/ticker/price')
    prices = response.json()

    return render_template('index.html', prices=prices)

if __name__ == '__main__':
    app.run(debug=True)
