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

def get_triangular_arbitrage_opportunities(prices):
    opportunities = []
    for coin1 in prices:
        for coin2 in prices:
            for coin3 in prices:
                if coin1 != coin2 and coin1 != coin3 and coin2 != coin3:
                    # Check if the coins form a valid triangular arbitrage opportunity
                    if coin2 in prices[coin1] and coin3 in prices[coin2] and coin1 in prices[coin3]:
                        # Calculate the potential profit after trading fees
                        profit = (1 / prices[coin1][coin2]) * (1 / prices[coin2][coin3]) * prices[coin3][coin1] * (1 - 0.001)**2 - 1

                        if profit > 0:
                            opportunities.append({'coins': f'{coin1} -> {coin2} -> {coin3} -> {coin1}',
                                                  'profit': profit})

    # Sort the opportunities by profit
    opportunities = sorted(opportunities, key=lambda x: x['profit'], reverse=True)

    return opportunities

def get_prices_matrix(prices):
    # Create a matrix of coin prices
    matrix = {}
    for coin1 in prices:
        matrix[coin1] = {}
        for coin2 in prices:
            if coin2 in prices[coin1]:
                matrix[coin1][coin2] = prices[coin1][coin2]
            elif coin1 != coin2:
                matrix[coin1][coin2] = None

    # Fill in the missing prices using transitive closure
    for k in matrix:
        for i in matrix:
            for j in matrix:
                if matrix[i][k] is not None and matrix[k][j] is not None:
                    if matrix[i][j] is None:
                        matrix[i][j] = matrix[i][k] * matrix[k][j]
                    else:
                        matrix[i][j] = min(matrix[i][j], matrix[i][k] * matrix[k][j])

    return matrix

 def get_triangular_arbitrage_opportunities_optimized(prices):
    opportunities = []
    prices_matrix = get_prices_matrix(prices)
    for coin1 in prices:
        for coin2 in prices:
            if coin2 in prices[coin1]:
                for coin3 in prices:
                    if coin3 in prices_matrix[coin2] and coin1 in prices_matrix[coin3]:
                        # Calculate the potential profit after trading fees
                        profit = (1 / prices_matrix[coin1][coin2]) * (1 / prices_matrix[coin2][coin3]) * prices_matrix[coin3][coin1] * (1 - 0.001)**2 - 1

                        if profit > 0:
                            opportunities.append({'coins': f'{coin1} -> {coin2} -> {coin3} -> {coin1}',
                                                  'profit': profit})

    # Sort the opportunities by profit
    opportunities = sorted(opportunities, key=lambda x: x['profit'], reverse=True)

    return opportunities


if __name__ == '__main__':
    prices = get_all_prices()
    opportunities = get_triangular_arbitrage_opportunities_optimized(prices)
    for opportunity in opportunities:
        print(opportunity['coins'], opportunity['profit'])
