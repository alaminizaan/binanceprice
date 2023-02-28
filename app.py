from flask import Flask, render_template
import ccxt
import itertools
import logging

# create Flask app object
app = Flask(__name__)

# create Binance exchange object
exchange = ccxt.binance({
    'enableRateLimit': True,  # enable rate-limiting
    'apiKey': 'OtmdN18Tgx7VjnLyD4Ulc7ooNUaS0ezw38EZtTXvz0Eln4LxePIGCjOC95WG80OG',  # replace with your API key
    'secret': 'ShmYzH63927bieEp6SgHTDXv3hlEdkiePHMsSpdXpbviKNJbGpPSS6M3YSTACq4u',  # replace with your API secret
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

        # render home page template with opportunities
        return render_template('home.html', opportunities=opportunities)
    except Exception as e:
        # log any errors that occur
        logging.error(e)
        return 'Error fetching market data'
# start Flask app
if __name__ == '__main__':
    app.run(debug=True)


