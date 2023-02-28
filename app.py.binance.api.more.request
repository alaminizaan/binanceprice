from flask import Flask, render_template
import requests
import itertools
import logging

# create Flask app object
app = Flask(__name__)

# define Binance API endpoint
api_endpoint = "https://api.binance.com/api/v3/ticker/price"

# define route for home page
@app.route('/')
def home():
    try:
        # fetch all available markets
        response = requests.get(api_endpoint)
        markets = response.json()

        # filter markets to include only those with USDT base and quote currencies
        usdt_markets = [market for market in markets if market['symbol'].endswith('USDT')]

        # generate all possible pairs of USDT markets
        usdt_pairs = itertools.combinations(usdt_markets, 2)

        # iterate over all USDT pairs and check for triangular arbitrage opportunities
        opportunities = []
        for pair1, pair2 in usdt_pairs:
            # get ticker data for all three pairs
            ticker1 = next((market for market in markets if market['symbol'] == pair1['symbol']), None)
            ticker2 = next((market for market in markets if market['symbol'] == pair2['symbol']), None)
            ticker3 = next((market for market in markets if market['symbol'] == pair1['symbol'].replace('USDT', pair2['symbol'][:-4])), None)

            # calculate potential profit from triangular arbitrage
            if all(ticker is not None for ticker in [ticker1, ticker2, ticker3]):
                profit = (1 / float(ticker1['price'])) * (1 / float(ticker2['price'])) * float(ticker3['price']) - 1

                # if profit is greater than 0, add the opportunity to the list
                if profit > 0:
                    opportunities.append({
                        'pair1': pair1['symbol'],
                        'pair2': pair2['symbol'],
                        'pair3': pair1['symbol'].replace('USDT', pair2['symbol'][:-4]),
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
