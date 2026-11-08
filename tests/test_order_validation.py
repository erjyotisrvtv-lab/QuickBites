"""Validate Orders input contract without requiring an external database."""
import importlib.util
import os
import tempfile
from pathlib import Path
from pydantic import ValidationError

# Unique module name prevents an import collision with services/catalog/main.py.
with tempfile.TemporaryDirectory() as folder:
    os.environ['DATABASE_URL']='sqlite:///'+str(Path(folder)/'orders.db')
    path=Path(__file__).parents[1]/'services'/'orders'/'main.py'
    spec=importlib.util.spec_from_file_location('quickbite_orders_contract',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    OrderRequest=module.OrderRequest

def test_valid_request():
    r=OrderRequest(customerId='  alice  ',restaurantId='r1',items=[{'menuItemId':'m1','quantity':2}])
    assert r.customerId=='alice'

def test_zero_quantity_rejected():
    try:OrderRequest(customerId='alice',restaurantId='r1',items=[{'menuItemId':'m1','quantity':0}])
    except ValidationError:pass
    else:raise AssertionError('Zero quantity should be rejected')
