import sys
from pathlib import Path
from fastapi.testclient import TestClient

CATALOG=Path(__file__).parents[1]/'services'/'catalog'
sys.path.insert(0,str(CATALOG))
from main import app  # noqa: E402
client=TestClient(app)

def test_restaurant_list():
    r=client.get('/restaurants')
    assert r.status_code==200
    assert len(r.json())==2
    assert 'items' not in r.json()[0]

def test_menu_and_health():
    assert client.get('/health').json()['status']=='ok'
    assert client.get('/restaurants/r1/menu').json()['items'][0]['priceCents']==1299
    assert client.get('/restaurants/invalid/menu').status_code==404
