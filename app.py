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

def calculate_arbitrage_opportunities(all_prices, trading_fee):
    opportunities = []
    # Check for arbitrage opportunities between all possible pairs of coins
    for symbol1 in all_prices:
        for symbol2 in all_prices:
            if symbol1 != symbol2 and symbol1.endswith('BTC') and symbol2.endswith('BTC'):
                price1 = all_prices[symbol1]
                price2 = all_prices[symbol2]
                # Calculate the implied price between the two coins via BTC
                implied_price = float(price2) / float(price1)
                # Calculate the potential profit after trading fees
                potential_profit = ((1 - trading_fee) * implied_price - 1) * 100
                # Check if the profit is greater than zero
                if potential_profit > 0:
                    opportunities.append((symbol1[:-3], symbol2[:-3], round(potential_profit, 2)))
    
    return opportunities

@app.route('/')
def show_arbitrage_opportunities():
    all_prices = get_all_prices()
    trading_fee = 0.001
    opportunities = calculate_arbitrage_opportunities(all_prices, trading_fee)
    
    # Create a list of strings containing the coin pair prices and the potential profits
    opportunities_str = []
    for opportunity in opportunities:
        symbol1, symbol2, profit = opportunity
        price1 = all_prices[symbol1+'BTC']
        price2 = all_prices[symbol2+'BTC']
        opportunity_str = f"{symbol1}-{symbol2}: {price1}, {price2} (profit: {profit}%)"
        if profit > 0:
            opportunity_str = f"<font color='green'>{opportunity_str}</font>"
        else:
            opportunity_str = f"<font color='red'>{opportunity_str}</font>"
        opportunities_str.append(opportunity_str)
    
    # Convert the list of strings to a single string with line breaks
    return '<br>'.join(opportunities_str)

if __name__ == '__main__':
    app.run(debug=True)
