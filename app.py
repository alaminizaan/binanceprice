import ccxt
import time

# define the symbol and the amount to trade
symbol = 'EOS/USDT'
amount = 100

# create an empty list to store the arbitrage opportunities
arbitrage_opportunities = []

# create a dictionary to store the fees for each exchange
fees = {}

# create an instance of the CCXT library
exchange = ccxt.Exchange()

# loop through all the exchanges that support EOS/USDT trading
for exchange_id in exchange.load_markets():
    # skip exchanges that do not have EOS/USDT trading pairs
    if symbol not in exchange.markets:
        continue

    # fetch the current order book for the trading pair
    order_book = exchange.fetch_order_book(symbol)

    # calculate the buy and sell prices taking into account the fees
    bid_price = order_book['bids'][0][0] * (1 - exchange.fees['trading']['taker'])
    ask_price = order_book['asks'][0][0] * (1 + exchange.fees['trading']['taker'])

    # calculate the arbitrage opportunity
    opportunity = (ask_price - bid_price) / bid_price * 100

    # store the arbitrage opportunity and the exchange name in a dictionary
    exchange_name = exchange.markets[symbol]['info']['exchange']
    arbitrage_opportunities.append({
        'exchange': exchange_name,
        'opportunity': opportunity
    })

    # store the fees for this exchange in the fees dictionary
    trading_fee = exchange.fees['trading']['taker']
    withdrawal_fee = exchange.fees['funding']['withdraw'][symbol.split('/')[0]]
    fees[exchange_name] = {
        'trading_fee': trading_fee,
        'withdrawal_fee': withdrawal_fee
    }

    # sleep for a short period to avoid rate limiting
    time.sleep(1)

# sort the list of arbitrage opportunities by descending order
arbitrage_opportunities = sorted(arbitrage_opportunities, key=lambda x: x['opportunity'], reverse=True)

# print the list of arbitrage opportunities
for opportunity in arbitrage_opportunities:
    print(f"{opportunity['exchange']}: {opportunity['opportunity']:.2f}%")

# print the fees for each exchange
for exchange_name, fee in fees.items():
    print(f"{exchange_name}: Trading fee - {fee['trading_fee']:.2%}, Withdrawal fee - {fee['withdrawal_fee']}")
