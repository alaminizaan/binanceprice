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

def calculate_arbitrage(symbol1, symbol2, all_prices):
    # Calculate arbitrage opportunity between two coins
    if symbol1 == symbol2:
        return 0
    
    if f"{symbol1}{symbol2}" in all_prices:
        price1 = all_prices[f"{symbol1}{symbol2}"]
        price2 = all_prices[f"{symbol2}{symbol1}"]
    elif f"{symbol2}{symbol1}" in all_prices:
        price1 = 1 / all_prices[f"{symbol2}{symbol1}"]
        price2 = 1 / all_prices[f"{symbol1}{symbol2}"]
    else:
        return 0
    
    fee = 0.001 # Trading fee is 0.1%
    buy_price = price1 * (1 + fee)
    sell_price = price2 * (1 - fee)
    profit_pct = (sell_price / buy_price - 1) * 100
    
    return profit_pct

@app.route('/')
def show_all_prices():
    all_prices = get_all_prices()
    # Convert dictionary to a string for displaying in the browser
    output = []
    for symbol, price in all_prices.items():
        output.append(f"{symbol}: {price}")
    
    # Calculate arbitrage opportunities
    arbitrage_opportunities = {}
    for symbol1, price1 in all_prices.items():
        for symbol2, price2 in all_prices.items():
            profit_pct = calculate_arbitrage(symbol1, symbol2, all_prices)
            if profit_pct != 0:
                arbitrage_opportunities[f"{symbol1}-{symbol2}"] = profit_pct
    
    # Sort opportunities by profit percentage in descending order
    sorted_opportunities = sorted(arbitrage_opportunities.items(), key=lambda x: x[1], reverse=True)
    
    # Add arbitrage opportunities to the output
    for opportunity in sorted_opportunities:
        symbol_pair = opportunity[0]
        profit_pct = opportunity[1]
        color = "green" if profit_pct > 0 else "red"
        output.append(f"{symbol_pair}: <font color='{color}'>{profit_pct:.2f}%</font>")
    
    return '<br>'.join(output)

if __name__ == '__main__':
    app.run(debug=True)
