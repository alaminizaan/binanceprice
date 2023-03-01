import requests

# Set the endpoint URL for the Coingecko API
endpoint = 'https://api.coingecko.com/api/v3/'

# Set the parameters for the EOS/USDT trading pair
symbol = 'eos'
currency = 'usdt'

# Get a list of all exchanges that support the EOS/USDT trading pair
url = endpoint + 'exchanges/list_by_pair'
params = {'id': symbol, 'vs_currency': currency}
response = requests.get(url, params=params)
exchanges = response.json()

# Loop through each exchange and get the current price for EOS/USDT
for exchange in exchanges:
    exchange_name = exchange['name']
    exchange_id = exchange['id']
    url = endpoint + 'simple/price'
    params = {'ids': exchange_id, 'vs_currencies': currency, 'include_24hr_change': 'true'}
    response = requests.get(url, params=params)
    data = response.json()
    
    # Calculate the price of EOS in USDT, including fees
    eos_price = data[exchange_id][currency]
    fee_url = endpoint + 'exchanges/' + exchange_id
    fee_response = requests.get(fee_url)
    fee_data = fee_response.json()
    trading_fees = fee_data['trade_volume_24h_btc_normalized']
    eos_price_with_fees = eos_price * (1 + trading_fees)
    
    # Print the current price of EOS on this exchange, including fees
    print(f"{exchange_name}: {eos_price_with_fees:.8f} USDT")
