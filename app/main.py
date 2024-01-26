from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

API_BUDA_URL_TICKER = "https://www.buda.com/api/v2/markets/{}/ticker"
API_BUDA_URL_MARKETS = "https://www.buda.com/api/v2/markets"

class AlertSpread(BaseModel):
    market_id: str
    spread: float

SETTED_ALERT_SPREAD = AlertSpread(market_id="", spread=0.0)

app = FastAPI()

#General function to do a request
def make_get_request(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Bad response from buda's server", response.status_code)
    return response.json()

def get_markets():
    try:
        markets = make_get_request(API_BUDA_URL_MARKETS)["markets"]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    return [market["id"] for market in markets]

def calculate_spread(min_ask: float, max_bid: float):
    return (min_ask - max_bid) 

#--Endpoints--

@app.get("/spreads/{market_id}")
def get_spread(market_id: str):
    try:
        ticker = make_get_request(API_BUDA_URL_TICKER.format(market_id.upper()))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
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
    markets = get_markets()
    spreads = []
    for market in markets:
        spread_result = get_spread(market)
        spreads.append(spread_result["spreads"])
    return {"spreads": spreads}

@app.post("/alert")
def alert_spread(alert: AlertSpread):
    SETTED_ALERT_SPREAD.market_id = alert.market_id
    SETTED_ALERT_SPREAD.spread = alert.spread

@app.get("/polling_alert_spread")
def get_polling():
    market_id = SETTED_ALERT_SPREAD.market_id
    if market_id == "":
        raise HTTPException(status_code=404, detail="Alert not founded. Use /alert endpoint.")
    spread_result = get_spread(market_id)
    if spread_result["spreads"]["spread"][0] >= SETTED_ALERT_SPREAD.spread:
        return {"alert": {"market-id": market_id, "actual-spread-greater": True}}
    return {"alert": {"market-id": market_id, "actual-spread-greater": False}}