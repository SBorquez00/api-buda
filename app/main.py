from fastapi import FastAPI
import requests

API_BUDA_URL_TICKER = "https://www.buda.com/api/v2/markets/{}/ticker"
API_BUDA_URL_MARKETS = "https://www.buda.com/api/v2/markets"

app = FastAPI()

#General function to do a request
def make_get_request(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Bad response from server", response.status_code)
    return response.json()

def get_markets():
    markets = make_get_request(API_BUDA_URL_MARKETS)["markets"]
    return [market["id"] for market in markets]

def calculate_spread(min_ask: float, max_bid: float):
    return (min_ask - max_bid) 

#--Endpoints--

@app.get("/spreads/{market_id}")
def get_spread(market_id: str):
    try:
        ticker = make_get_request(API_BUDA_URL_TICKER.format(market_id.upper()))
    except Exception as e:
        return {"error": str(e)}
    currency = ticker["ticker"]["min_ask"][1]
    min_ask = float(ticker['ticker']['min_ask'][0])
    max_bid = float(ticker['ticker']['max_bid'][0])
    spread = calculate_spread(min_ask, max_bid)

    return {"spreads": {
        "market_id": market_id,
        "spread": [spread, currency]
        }}

@app.get("/spreads")
def get_all_spreads():
    try:
        markets = get_markets()
    except Exception as e:
        return {"error": str(e)}
    spreads = []
    for market in markets:
        spread_result = get_spread(market)
        spreads.append(spread_result["spreads"])
    return {"spreads": spreads}