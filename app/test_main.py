from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get_spread():
    response = client.get("/spreads/btc-clp")
    assert response.status_code == 200
    #Content tests
    response = response.json()
    assert "spreads" in response
    assert response["spreads"]["spread"][1] == "CLP"
    assert isinstance(response["spreads"]["spread"][0], float)

def test_get_all_spreads():
    response = client.get("/spreads")
    assert response.status_code == 200

    response = response.json()
    #List tests
    assert "spreads" in response
    assert len(response["spreads"]) > 0
    #Content tests
    assert "market_id" in response["spreads"][0]
    assert "spread" in response["spreads"][0]
    assert response["spreads"][0]["spread"][1] == "CLP"
    assert isinstance(response["spreads"][0]["spread"][0], float)

def test_set_alert_spread():
    response = client.post("/alert", json={"market_id": "btc-clp", "spread": 100})
    assert response.status_code == 200

def test_get_polling():
    #set alert
    client.post("/alert", json={"market_id": "btc-clp", "spread": 0})
    #polling
    response = client.get("/polling_alert_spread")
    assert response.status_code == 200
    response = response.json()
    assert response["alert"]["market-id"] == "btc-clp"
    assert response["alert"]["actual-spread-greater"] == True

def test_get_polling_without_alert():
    #reset alert to default value
    client.post("/alert", json={"market_id": "", "spread": 0.0})
    response = client.get("/polling_alert_spread")
    assert response.status_code == 404
    response = response.json()
    assert response["detail"] == "Alert not founded. Use /alert endpoint."

