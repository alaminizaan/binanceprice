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

def show_arbitrage_opportunity():
    all_prices = get_all_prices()
    opportunities = []
    
    # Scan all coin pairs for triangular arbitrage opportunities
    for coin1 in all_prices:
        for coin2 in all_prices:
            for coin3 in all_prices:
                if coin1 != coin2 and coin1 != coin3 and coin2 != coin3:
                    # Calculate the potential profit after trading fees
                    profit = (1 / all_prices[coin1]) * (1 / all_prices[coin2]) * all_prices[coin3] * (1 - 0.001)**2 - 1
                    
                    if profit > 0:
                        opportunities.append({'coins': f'{coin1} -> {coin2} -> {coin3} -> {coin1}',
                                              'profit': profit})
    
    # Sort the opportunities by profit
    opportunities = sorted(opportunities, key=lambda x: x['profit'], reverse=True)
    
    # Convert the opportunities to a string for displaying in the browser
    opportunities_str = '<br>'.join([f"<span style='color:green'>{o['coins']} - {o['profit']*100:.2f}%</span>"
                                     if o['profit']*100 > 0 else f"<span style='color:red'>{o['coins']} - {o['profit']*100:.2f}%</span>"
                                     for o in opportunities])
    
    return opportunities_str

@app.route('/')
def show_all_prices():
    all_prices_str = '<br>'.join([f'{symbol}: {price:.2f} USDT' for symbol, price in get_all_prices().items()])
    return f"<h2>All Prices:</h2>{all_prices_str}<br><br><h2>Triangular Arbitrage Opportunities:</h2>{show_arbitrage_opportunity()}"

if __name__ == '__main__':
    app.run(debug=True)
