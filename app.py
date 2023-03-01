from flask import Flask, jsonify
import ccxt

app = Flask(__name__)

# Fetch all exchanges that support EOS/USDT trading pair
exchanges = {}
for exchange_id in ccxt.exchanges:
    try:
        exchange = getattr(ccxt, exchange_id)()
        markets = exchange.load_markets()
        if 'EOS/USDT' in markets:
            exchanges[exchange_id] = exchange
    except Exception as e:
        print(f"Failed to load exchange {exchange_id}: {e}")

@app.route('/arbitrage')
def find_arbitrage_opportunity():
    buy_price = None
    sell_price = None
    for exchange_id, exchange in exchanges.items():
        try:
            orderbook = exchange.fetch_order_book('EOS/USDT')
            if orderbook['bids'] and orderbook['asks']:
                current_buy_price = orderbook['bids'][0][0]
                current_sell_price = orderbook['asks'][0][0]
                if buy_price is None or current_buy_price > buy_price:
                    buy_price = current_buy_price
                    buy_exchange = exchange_id
                if sell_price is None or current_sell_price < sell_price:
                    sell_price = current_sell_price
                    sell_exchange = exchange_id
        except Exception as e:
            print(f"Failed to fetch orderbook from {exchange_id}: {e}")
    
    if buy_price is not None and sell_price is not None:
        spread = sell_price - buy_price
        return jsonify({
            'buy_exchange': buy_exchange,
            'buy_price': buy_price,
            'sell_exchange': sell_exchange,
            'sell_price': sell_price,
            'spread': spread
        })
    else:
        return jsonify({'message': 'No arbitrage opportunities found.'})

if __name__ == '__main__':
    app.run()
