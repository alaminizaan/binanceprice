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

# define function to get USD equivalent of a given symbol
def get_usd_equivalent(symbol, quantity):
    # if symbol is already USD, return the quantity
    if symbol == 'USDT':
        return quantity
    
    # get ticker data for symbol's USD pair
    ticker = exchange.fetch_ticker(symbol+'/USDT')
    
    # calculate USD equivalent of quantity
    usd_equivalent = quantity * ticker['last']
    
    return usd_equivalent

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

            # calculate potential profit from triangular arbitrage in USD
            profit_usd = get_usd_equivalent(pair1['quote'], 1) * get_usd_equivalent(pair2['quote'], 1) * get_usd_equivalent(pair2['base'], ticker3['bid']) - get_usd_equivalent(pair1['base'], 1)

            # if profit is greater than 0, add the opportunity to the list
            if profit_usd > 0:
                opportunities.append({
                    'pair1': pair1['symbol'],
                    'pair2': pair2['symbol'],
                    'pair3': pair1['symbol'].replace(pair1['quote'], pair2['base']),
                    'profit_usd': profit_usd
                })

        # sort opportunities by profit in descending order
        opportunities.sort(key=lambda x: x['profit_usd'], reverse=True)

        # get current prices for all markets and convert to USD
        tickers = exchange.fetch_tickers()
        prices_usd = {symbol: get_usd_equivalent(ticker['symbol'], ticker['last']) for symbol, ticker in tickers.items()}

        # render home page template with opportunities and prices in USD
        return render_template('home.html', opportunities=opportunities, prices=prices_usd)
    except Exception as e:
        # log any errors that occur
        logging.error(e)
        return 'Error fetching market data'

# define route for getting real-time prices as JSON
@app.route('/prices')
def get_prices():
    try:
        # fetch all available markets
        markets = exchange.load_markets()

        # filter markets to include only those with USD base and quote currencies
        usd_markets = [market for market in markets if isinstance(market, dict) and market.get('quote') == 'USD' and market.get('active')]

        # get current prices for all USD markets
        tickers = exchange.fetch_tickers([market['symbol'] for market in usd_markets])
        prices = {}
        for symbol, ticker in tickers.items():
            # convert price to USD if quote currency is not already USD
            if ticker['quote'] != 'USD':
                usd_pair = f"{ticker['quote']}/USD"
                usd_ticker = exchange.fetch_ticker(usd_pair)
                prices[symbol] = ticker['last'] * usd_ticker['last']
            else:
                prices[symbol] = ticker['last']

        # return prices as JSON
        return jsonify(prices)
    except Exception as e:
        # log any errors that occur
        logging.error(e)
        return 'Error fetching market data'
# start Flask app
if __name__ == '__main__':
    app.run(debug=True)
