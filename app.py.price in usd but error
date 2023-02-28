from flask import Flask, render_template, jsonify
import ccxt
import itertools
import logging
import time

# create Flask app object
app = Flask(__name__)

# create Binance exchange object
exchange = ccxt.binance({
    'enableRateLimit': True,  # enable rate-limiting
    'apiKey': 'YOUR_BINANCE_API_KEY',  # replace with your API key
    'secret': 'YOUR_BINANCE_API_SECRET',  # replace with your API secret
})

# define route for home page
@app.route('/')
def home():
    try:
        # fetch all available markets
        markets = exchange.load_markets()

        # filter markets to include only those with USDT base and quote currencies
        usdt_markets = [market for market in markets if isinstance(market, dict) and market.get('quote') == 'USDT' and market.get('active')]

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

            # if profit is greater than 0, add the opportunity to the list
            if profit > 0:
                opportunities.append({
                    'pair1': pair1['symbol'],
                    'pair2': pair2['symbol'],
                    'pair3': pair1['symbol'].replace(pair1['quote'], pair2['base']),
                    'profit': profit
                })

        # sort opportunities by profit in descending order
        opportunities.sort(key=lambda x: x['profit'], reverse=True)

        # get current prices for all markets
        tickers = exchange.fetch_tickers()
        usd_tickers = {}
        for symbol, ticker in tickers.items():
            # convert price to USD if it's not already in USD
            if ticker['symbol'].endswith('USD'):
                usd_tickers[symbol] = ticker['last']
            else:
                # construct USD symbol and fetch ticker for that symbol
                usd_symbol = ticker['symbol'] + '/USD'
                usd_ticker = exchange.fetch_ticker(usd_symbol)
                usd_tickers[symbol] = ticker['last'] * usd_ticker['last']

        # render home page template with opportunities and USD prices
        return render_template('home.html', opportunities=opportunities, prices=usd_tickers)
    except Exception as e:
        # log any errors that occur
        logging.error(e)
        return 'Error fetching market data'

# define route for getting real-time USD prices as JSON
@app.route('/prices')
def get_prices():
    try:
        # fetch all available markets
        markets = exchange.load_markets()

        # filter markets to include only those with USD base and quote currencies
        usd_markets = [market for market in markets if isinstance(market, dict) and market.get('quote') == 'USD' and market.get('active')]

        # get current prices for all USD markets
        tickers = exchange.fetch_tickers([market['symbol'] for market in usd_markets])
        usd_tickers = {symbol: ticker['last'] for symbol, ticker in tickers.items()}

        # return USD prices as JSON
        return jsonify(usd_tickers)
    except Exception as e:
        # log any errors that occur
        logging.error(e)
        return 'Error fetching market data'
  
# start Flask app
if __name__ == '__main__':
    app.run(debug=True)
