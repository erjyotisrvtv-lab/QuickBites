"""Integration check against a running QuickBite Gateway. Exit !=0 on any failure."""
import os
import sys
import uuid
import httpx

BASE=os.environ.get('QUICKBITE_URL','http://127.0.0.1:8080').rstrip('/')

def require(cond,message):
    if not cond:raise AssertionError(message)

def main():
    with httpx.Client(base_url=BASE,timeout=15) as client:
        checks=['/health','/api/catalog/restaurants','/api/catalog/restaurants/r1/menu','/api/orders/health','/api/deliveries/health']
        for path in checks:
            r=client.get(path)
            require(r.status_code==200,f'{path}: {r.status_code} {r.text}')
            print('PASS',path)
        order_payload={'customerId':'smoke-'+uuid.uuid4().hex[:8],'restaurantId':'r1',
                       'items':[{'menuItemId':'m1','quantity':2},{'menuItemId':'m3','quantity':1}]}
        order=client.post('/api/orders/orders',json=order_payload)
        require(order.status_code==201,f'Order failed: {order.status_code} {order.text}')
        oid=order.json()['id']
        require(order.json()['totalCents']==2997,'Incorrect server-calculated order total')
        require(client.get(f'/api/orders/orders/{oid}').status_code==200,'Order lookup failed')
        require(client.get('/api/orders/orders?limit=2&offset=0').status_code==200,'Order listing failed')
        print('PASS create/list/read order; totalCents=2997')
        bad=client.post('/api/orders/orders',json={'customerId':'tester','restaurantId':'r1',
                        'items':[{'menuItemId':'m-not-found','quantity':1}]})
        require(bad.status_code==422,f'Invalid menu item response: {bad.status_code}')
        print('PASS invalid menu item rejected')
        delivery=client.post('/api/deliveries/deliveries',json={'orderId':oid,'customerAddress':'Academic lab'})
        require(delivery.status_code==201,f'Delivery failed: {delivery.status_code} {delivery.text}')
        did=delivery.json()['id']
        require(client.get(f'/api/deliveries/deliveries/{did}').status_code==200,'Delivery lookup failed')
        repeated=client.post('/api/deliveries/deliveries',json={'orderId':oid,'customerAddress':'Academic lab'})
        require(repeated.status_code==409,f'Duplicate delivery must be 409: {repeated.status_code}')
        print('PASS create/read delivery and 409 duplicate handling')
    print('SUCCESS – all QuickBite smoke tests passed')
if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAILED:',exc,file=sys.stderr);sys.exit(1)
