from flask import Flask, render_template
import ccxt
import itertools

# create Flask app object
app = Flask(__name__)

# create Binance exchange object
exchange = ccxt.binance()

# define route for home page
@app.route('/')
def home():
    # fetch all available markets
    markets = exchange.load_markets()

    # filter markets to include only those with USDT base and quote currencies
    usdt_markets = [market for market in markets if market['quote'] == 'USDT' and market['active']]

    # generate all possible pairs of USDT markets
    usdt_pairs = itertools.combinations(usdt_markets, 2)

    # iterate over all USDT pairs and check for triangular arbitrage opportunities
    opportunities = []
    for pair1, pair2 in usdt_pairs:
        # get ticker data for all three pairs
        ticker1 = exchange.fetch_ticker(pair1['symbol'])
        ticker2 = exchange.fetch_ticker(pair2['symbol'])
        ticker3 = exchange.fetch_ticker(pair1['symbol'].replace(pair1['quote'], pair2['base']))

        # calculate potential profit from triangular arbitrage
        profit = (1 / ticker1['ask']) * (1 / ticker2['ask']) * ticker3['bid'] - 1

        # account for trading fees
        profit -= (0.001 * 3)

        # check if potential profit is positive and greater than a minimum threshold
        if profit > 0.001:
            opportunities.append((pair1['symbol'], pair2['symbol'], pair1['symbol'].replace(pair1['quote'], pair2['base']), profit))

    # render template with list of opportunities
    return render_template('home.html', opportunities=opportunities)

# start Flask app
if __name__ == '__main__':
    app.run(debug=True)
