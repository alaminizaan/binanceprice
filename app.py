from flask import Flask
import requests

app = Flask(__name__)

# list of coins and quantities you own
coins = {
    'BTC': 2.5,
    'ETH': 10,
    'LTC': 5,
    'XRP': 1000,
    'BCH': 3
}

# function to get price of a given coin from Binance API
def get_price(coin):
    url = f'https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT'
    response = requests.get(url)
    data = response.json()
    price = float(data['price'])
    return price

# route to display prices of all coins and quantity owned
@app.route('/')
def show_prices():
    prices = []
    for coin in coins:
        price = get_price(coin)
        value = price * coins[coin]
        prices.append(f"{coin}: ${price:.2f} ({coins[coin]} owned, value: ${value:.2f})")
    return '<br>'.join(prices)

if __name__ == '__main__':
    app.run(debug=True)
