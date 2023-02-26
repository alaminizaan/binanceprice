import requests
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url)
    data = response.json()
    btc_price = data['price']
    return f'The current price of BTC is {btc_price} USD'

if __name__ == '__main__':
    app.run(debug=True)
