import requests
from flask import Flask

app = Flask(__name__)

def get_all_prices():
    # Fetch all ticker prices from Binance API
    api_url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(api_url)
    prices = response.json()

    # Create a dictionary with coin symbols as keys and prices as values
    all_prices = {}
    for price in prices:
        symbol = price['symbol']
        price = float(price['price'])
        if symbol.endswith('USDT'):
            all_prices[symbol[:-4]] = price
        elif symbol.endswith('USD'):
            all_prices[symbol[:-3]] = price

    return all_prices

@app.route('/')
def show_all_prices():
    all_prices = get_all_prices()
    # Convert dictionary to a string for displaying in the browser
    all_prices_str = '<br>'.join([f'{symbol}: {price:.2f} USDT' for symbol, price in all_prices.items()])
    return all_prices_str

if __name__ == '__main__':
    app.run(debug=True)
