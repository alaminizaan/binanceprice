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
        all_prices[symbol] = price
    
    return all_prices

def calculate_arbitrage_opportunity(prices):
    opportunities = []
    for symbol1, price1 in prices.items():
        for symbol2, price2 in prices.items():
            for symbol3, price3 in prices.items():
                if symbol1[-3:] == symbol2[:3] and symbol2[-3:] == symbol3[:3] and symbol3[-3:] == symbol1[:3]:
                    # Found a triangular arbitrage opportunity
                    cross_rate = price1 * price2 / price3
                    implied_rate = cross_rate * 0.997 ** 3 # Apply 0.1% trading fee to each leg of the trade
                    profit = (implied_rate - 1) * 100 # Calculate profit as a percentage
                    opportunities.append((symbol1, symbol2, symbol3, profit))
    return opportunities

@app.route('/')
def show_arbitrage_opportunity():
    all_prices = get_all_prices()
    opportunities = calculate_arbitrage_opportunity(all_prices)
    if not opportunities:
        return 'No triangular arbitrage opportunities found.'
    else:
        opportunities_str = '<br>'.join([f'{s1} -> {s2} -> {s3}: <span style="color:{color};">{profit:.2f}%</span>' \
                                         for s1, s2, s3, profit, color in [(s1, s2, s3, p, 'green') \
                                                                           if p > 0 else (s1, s2, s3, p, 'red') \
                                                                           for s1, s2, s3, p in opportunities]])
        return opportunities_str

if __name__ == '__main__':
    app.run(debug=True)
