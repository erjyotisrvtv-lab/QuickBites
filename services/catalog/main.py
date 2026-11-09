from fastapi import FastAPI, HTTPException

app = FastAPI(title="QuickBite Catalog Service", version="1.0.0")
# The catalog is intentionally sample data; persistent storage belongs to a later enhancement.
RESTAURANTS = [
    {"id":"r1", "name":"Green Garden", "cuisine":"Healthy", "items":[
        {"id":"m1", "name":"Harvest Bowl", "priceCents":1299},
        {"id":"m2", "name":"Avocado Toast", "priceCents":899},
        {"id":"m3", "name":"Lemonade", "priceCents":399},
    ]},
    {"id":"r2", "name":"Corner Pizza", "cuisine":"Italian", "items":[
        {"id":"m4", "name":"Margherita Pizza", "priceCents":1499},
        {"id":"m5", "name":"Garlic Knots", "priceCents":599},
        {"id":"m6", "name":"Tiramisu", "priceCents":699},
    ]},
]

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/live')
def live():
    return {'status':'ok'}

@app.get('/restaurants')
def list_restaurants():
    return [{k:v for k,v in r.items() if k!='items'} for r in RESTAURANTS]

@app.get('/restaurants/{restaurant_id}/menu')
def get_menu(restaurant_id: str):
    restaurant = next((r for r in RESTAURANTS if r['id']==restaurant_id), None)
    if restaurant is None:
        raise HTTPException(status_code=404,detail='Restaurant not found')
    return restaurant
