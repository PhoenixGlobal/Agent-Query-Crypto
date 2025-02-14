import typing
import requests


#info fetcher functions
#get current coin price 
def fetch_coin_price(coin_name,timestamp):
    price_url = "https://phoenix.global/agent/api/crypto/symbolPrice"
    params = {
        "symbol": coin_name,
        "time": timestamp
    }

    try:
        response = requests.get(price_url,params=params)
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print(f"request failed: {e}")
        return None
    
#irrevelent to time 
#search market cap
def fetch_coin_marketcap(coin_name):
    marketcap_url = "https://phoenix.global/agent/api/crypto/market-cap"
    headers = {
        "accept": "application/json",
        "Token": "OYa923yQ>?3229!nMZ"
    }
    params = {
        "symbol": coin_name
    }

    try:
        response = requests.get(marketcap_url, headers = headers,params=params)
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print(f"request failed: {e}")
        return None
    
#get supply info
def fetch_coin_supply_info(coin_name):
    supply_info_url = "https://phoenix.global/agent/api/crypto/supply-info"
    headers = {
        "accept": "application/json",
        "Token": "OYa923yQ>?3229!nMZ"
    }
    params = {
        "symbol": coin_name
    }

    try:
        response = requests.get(supply_info_url, headers = headers,params=params)
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print(f"request failed: {e}")
        return None

#get order book
def fetch_coin_orderbook(coin_name):
    orderbook_url = "https://phoenix.global/agent/api/crypto/order-book"
    headers = {
        "accept": "application/json",
        "Token": "OYa923yQ>?3229!nMZ"
    }
    params = {
        "symbol": coin_name
    }

    try:
        response = requests.get(orderbook_url, headers = headers,params=params)
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print(f"request failed: {e}")
        return None
    
    
    
#get historical price in 24hour, 7 days, and 30 days
def fetch_coin_historical_price(coin_name,time_window:int):
    historical_price_url = "https://phoenix.global/agent/api/crypto/historical-price"
    headers = {
        "accept": "application/json",
        "Token": "OYa923yQ>?3229!nMZ"
    }
    params = {
        "symbol": coin_name,
        "timeDimension": time_window
    }
    try:
        response = requests.get(historical_price_url, headers = headers,params=params)
        response.raise_for_status()  
        data = response.json() 
        return data
    except requests.exceptions.RequestException as e:
        print(f"request failed: {e}")
        return None
    
