from fastapi.testclient import TestClient
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("quickbite_catalog_testmod", Path(__file__).parents[1]/"main.py")
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
app=module.app

def test_catalog_and_missing_restaurant():
    with TestClient(app) as c:
        assert c.get('/restaurants').status_code == 200
        assert c.get('/restaurants/r1/menu').json()['items'][0]['priceCents'] == 1299
        assert c.get('/restaurants/missing/menu').status_code == 404
