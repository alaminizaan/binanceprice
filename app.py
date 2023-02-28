from flask
import Flask, render_template, jsonify
import ccxt
import itertools
import logging
import time

# create Flask app object
app = Flask(__name__)

# create list of exchange IDs to use
exchange_ids = ['binance', 'kraken', 'bitstamp', 'coinbasepro', 'poloniex', 'bitfinex', 'bittrex', 'gemini', 'hitbtc', 'huobipro',
    'kucoin', 'okex', 'bitmart', 'bitforex', 'gateio', 'ftx', 'bibox', 'digifinex', 'bitmax', 'bitz', 'bitrue', 'liquid',
    'bybit', 'deribit', 'phemex', 'binanceus', 'coinex', 'probitkr', 'bitbank', 'bitflyer', 'ftxus', 'ftxjp', 'okcoin',
    'bitso', 'bitvavo', 'coinone', 'huobijp', 'upbit', 'krakenfutures', 'bitget', 'bitkub', 'btse', 'currencycom',
    'bequant', 'cryptocom', 'exmo', 'indodax', 'krakenus', 'latoken', 'mxc', 'okexkr', 'okexin', 'rightbtc', 'zb',
    'binancedex', 'bitribe', 'bkex', 'btcalpha', 'chiliz', 'cointiger', 'digifinexv2', 'gdax', 'gopax', 'huobiru',
    'idex', 'lbank', 'mercatox', 'probit', 'tokok', 'trading212', 'tradeogre', 'yobit', 'bilaxy', 'bw', 'cobinhood',
    'crex24', 'dragonex', 'exx', 'fcoin', 'finexbox', 'folgory', 'galois', 'hotbit', 'indodax2', 'liquid2', 'maxmex',
    'p2pb2b', 'phemex2', 'stex', 'topbtc', 'zbg'
]

# create dictionary of exchanges
exchanges = {
    exchange_id: ccxt.__dict__[exchange_id]({
        'enableRateLimit': True,
        #enable rate - limiting 'apiKey': 'YOUR_API_KEY',
        #replace with your API key 'secret': 'YOUR_API_SECRET',
        #replace with your API secret
    }) for exchange_id in exchange_ids
}

#
define route
for home page@ app.route('/')
def home():
    try: #initialize empty list to store opportunities across all exchanges
all_opportunities = []

# iterate over all exchanges
for exchange_id in ccxt.exchanges:
    try: #create exchange object
exchange = getattr(ccxt, exchange_id)({
    'enableRateLimit': True,
    #enable rate - limiting
})

# fetch all available markets
markets = exchange.load_markets()

# filter markets to include only those with USDT base and quote currencies
usdt_markets = [market
    for market in markets
    if isinstance(market, dict) and market.get('quote') == 'USDT'
    and market.get('active')
]

# generate all possible pairs of USDT markets
usdt_pairs = itertools.combinations(usdt_markets, 2)

# iterate over all USDT pairs and check
for triangular arbitrage opportunities
opportunities = []
for pair1, pair2 in usdt_pairs: #get ticker data
for all three pairs
ticker1 = exchange.fetch_ticker(pair1['symbol'])
ticker2 = exchange.fetch_ticker(pair2['symbol'])
ticker3 = exchange.fetch_ticker(pair1['symbol'].replace(pair1['quote'], pair2['base']))

# calculate potential profit from triangular arbitrage
profit = (1 / ticker1['ask']) * (1 / ticker2['ask']) * ticker3['bid'] - 1

#
if profit is greater than 0, add the opportunity to the list
if profit > 0:
    opportunities.append({
        'exchange': exchange_id,
        'pair1': pair1['symbol'],
        'pair2': pair2['symbol'],
        'pair3': pair1['symbol'].replace(pair1['quote'], pair2['base']),
        'profit': profit
    })

# sort opportunities by profit in descending order
opportunities.sort(key = lambda x: x['profit'], reverse = True)

# add opportunities
for this exchange to the all_opportunities list
all_opportunities.extend(opportunities)

except Exception as e: #log any errors that occur
while processing this exchange
logging.error(f "Error processing {exchange_id}: {e}")

# sort all opportunities by profit in descending order
all_opportunities.sort(key = lambda x: x['profit'], reverse = True)

# get current prices
for all USDT markets across all exchanges
tickers = {}
for exchange_id in ccxt.exchanges:
    try: #create exchange object
exchange = getattr(ccxt, exchange_id)({
    'enableRateLimit': True,
    #enable rate - limiting
})

# fetch all available markets
markets = exchange.load_markets()

# filter markets to include only those with USDT base and quote currencies
usdt_markets = [market
    for market in markets
    if isinstance(market, dict) and market.get('quote') == 'USDT'
    and market.get('active')
]

# get current prices
for all USDT markets on this exchange
exchange_tickers = exchange.fetch_tickers([market['symbol']
    for market in usdt_markets
])

# update the main tickers dictionary with the prices from this exchange
for symbol, ticker in exchange_tickers.items():
    tickers[f "{exchange_id}:{symbol}"] = ticker['last']

except Exception as e: #log any errors that occur
while processing this exchange
logging.error(f "Error processing {exchange_id}: {e}")

# filter markets to include only those with USDT base and quote currencies
usdt_markets = [market
    for market in markets
    if isinstance(market, dict) and market.get('quote') == 'USDT'
    and market.get('active')
]

# get current prices
for all USDT markets
tickers = {
    symbol: price
    for symbol,
    price in tickers.items() if symbol.split(':')[1] in [market['symbol']
        for market in usdt_markets
    ]
}

#
generate all possible pairs of USDT markets
usdt_pairs = itertools.combinations(usdt_markets, 2)

# iterate over all USDT pairs and check
for triangular arbitrage opportunities
opportunities = []
for pair1, pair2 in usdt_pairs: #get ticker data
for all three pairs
ticker1 = tickers[f "{pair1['symbol']}:USDT"]
ticker2 = tickers[f "{pair2['symbol']}:USDT"]
ticker3 = tickers[f "{pair1['symbol'].replace(pair1['quote'], pair2['base'])}:USDT"]

# calculate potential profit from triangular arbitrage
profit = (1 / ticker1) * (1 / ticker2) * ticker3 - 1

#
if profit is greater than 0, add the opportunity to the list
if profit > 0:
    opportunities.append({
        'pair1': pair1['symbol'],
        'pair2': pair2['symbol'],
        'pair3': pair1['symbol'].replace(pair1['quote'], pair2['base']),
        'profit': profit
    })

# sort opportunities by profit in descending order
opportunities.sort(key = lambda x: x['profit'], reverse = True)

# get current prices
for all markets
prices = {
    symbol: ticker['last']
    for symbol,
    ticker in tickers.items()
}

#
render home page template with opportunities and prices
return render_template('home.html', opportunities = opportunities, prices = prices)
except Exception as e: #log any errors that occur
logging.error(e)
return 'Error fetching market data'#
define route
for getting real - time prices as JSON@ app.route('/prices')
def get_prices():
    try: #fetch all available markets
markets = list(tickers.keys())

# fetch the current prices
for all markets
prices = {}
for market in markets:
    prices[market] = tickers[market]

#
return the prices as JSON
return jsonify(prices)

except Exception as e: #log any errors that occur
while fetching prices
logging.error(f "Error fetching prices: {e}")
return jsonify({
    'error': str(e)
}), 500# start Flask appp
if __name__ == '__main__':
    app.run(debug = True)
