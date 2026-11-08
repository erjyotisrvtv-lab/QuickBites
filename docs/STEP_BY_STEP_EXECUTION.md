# Step-by-step QuickBite execution — Windows PowerShell / macOS Terminal

## Step 1 – Confirm tools
Check `python --version`, `docker --version`, `docker compose version`, `minikube version`, `kubectl version --client`, `git --version`.
You may use Python-only local mode before Docker / WSL2 / Hyper-V becomes available. **Python-only execution does not satisfy the Minikube portion of the assignment.**

## Step 2 – Code/repository layout
Four independently testable service roots: `services/catalog`, `services/orders`, `services/delivery`, `services/gateway`. Infrastructure: `docker-compose.yml`, `deploy/kubernetes/*.yaml`. The supplied ZIP combines them for university submission; put each service folder in its **own Git repository** before submitting.

## Step 3 – Local run (works without Docker)
Open terminal at the folder containing `run_local.py`:

**Windows PowerShell**
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe run_local.py
```
If Python 3.12 is not installed, use `py -m venv .venv` with Python 3.10+.

**macOS/Linux**
```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python run_local.py
```
The launcher starts Catalog 3001, Orders 3002, Delivery 3003 and Gateway 8080. It stores SQLite development data under `data/`. Leave this terminal running.

## Step 4 – Browser / Swagger / Postman
Open `http://127.0.0.1:8080/` and `http://127.0.0.1:8080/docs`.
In a second terminal run `python scripts/smoke_test.py` and `pytest -q`. Import `postman/QuickBite.postman_collection.json` in Postman.

### Commands/queries to demonstrate
`GET http://127.0.0.1:8080/api/catalog/restaurants`
`GET http://127.0.0.1:8080/api/catalog/restaurants/r1/menu`
`POST http://127.0.0.1:8080/api/orders/orders`
```json
{"customerId":"student-101","restaurantId":"r1","items":[{"menuItemId":"m1","quantity":2},{"menuItemId":"m3","quantity":1}]}
```
Expected total: `2 * 1299 + 399 = 2997 cents` (₹29.97). Copy returned order `id`.
`GET http://127.0.0.1:8080/api/orders/orders`
`GET http://127.0.0.1:8080/api/orders/orders/<order-id>`
`POST http://127.0.0.1:8080/api/deliveries/deliveries`
```json
{"orderId":"<order-id>","customerAddress":"BITS Pilani Academic Demo Address"}
```
Then query `GET http://127.0.0.1:8080/api/deliveries/deliveries/<delivery-id>`. Repeat create-delivery to document HTTP 409 duplicate prevention.

## Step 5 – Docker Compose (actual separate containers)
Start Docker Desktop. In Windows, ensure WSL2 / Virtual Machine Platform enabled using an **Administrator** terminal if necessary, reboot, then start Docker Desktop. Do not claim Docker deployment until the engine is actually running.
```sh
docker compose config
docker compose up --build -d
docker compose ps
docker compose logs --tail=50 gateway orders delivery catalog
python scripts/smoke_test.py
```
See distinct `catalog`, `orders`, `delivery`, `gateway`, `orders-db`, `delivery-db` containers. Record `docker compose ps` and successful smoke output. Stop with `docker compose down` (do not use `-v` unless you want to delete databases).

## Step 6 – Minikube and Kubernetes **mandatory**
Install working Docker driver, Minikube and kubectl. If the minikube command is not found, install Minikube first and reopen terminal. Start using `minikube start --driver=docker --cpus=4 --memory=6144`. A resource-constrained host may require fewer replicas/resources for the demo.

Enable CPU metrics:
```sh
minikube addons enable metrics-server
```
Build every service image **into Minikube** (from the root folder):
```sh
minikube image build -t quickbite/catalog:local -f services/catalog/Dockerfile services/catalog
minikube image build -t quickbite/orders:local -f services/orders/Dockerfile services/orders
minikube image build -t quickbite/delivery:local -f services/delivery/Dockerfile services/delivery
minikube image build -t quickbite/gateway:local -f services/gateway/Dockerfile services/gateway
```
Apply namespace and demo secrets first, then the rest:
```sh
kubectl apply -f deploy/kubernetes/00-namespace.yaml
kubectl apply -f deploy/kubernetes/01-secret-demo.yaml
kubectl apply -f deploy/kubernetes/02-databases.yaml
kubectl apply -f deploy/kubernetes/03-catalog.yaml
kubectl apply -f deploy/kubernetes/04-orders.yaml
kubectl apply -f deploy/kubernetes/05-delivery.yaml
kubectl apply -f deploy/kubernetes/06-gateway.yaml
kubectl apply -f deploy/kubernetes/07-hpa.yaml
kubectl apply -f deploy/kubernetes/08-pdb.yaml
```
Wait for deployments:
```sh
kubectl -n food-delivery rollout status statefulset/orders-db --timeout=180s
kubectl -n food-delivery rollout status statefulset/delivery-db --timeout=180s
kubectl -n food-delivery rollout status deployment/catalog --timeout=180s
kubectl -n food-delivery rollout status deployment/orders --timeout=180s
kubectl -n food-delivery rollout status deployment/delivery --timeout=180s
kubectl -n food-delivery rollout status deployment/gateway --timeout=180s
kubectl -n food-delivery get deploy,statefulset,pods,svc,pvc,hpa,pdb
```
Publish gateway locally (leave running in a terminal):
```sh
kubectl -n food-delivery port-forward service/gateway 8080:8080
```
In another terminal run `python scripts/smoke_test.py`; open `http://127.0.0.1:8080/`.

## Step 7 – Kubernetes dashboard and scaling evidence
```sh
minikube addons enable dashboard
minikube dashboard
kubectl -n food-delivery get hpa
kubectl -n food-delivery top pods
kubectl -n food-delivery get pods -o wide
```
In the dashboard change namespace filter to `food-delivery`. Capture Workloads → Deployments and Pods, and Resource view where available. Show HPA min=2 max=10 and utilization target=70%. Since workload scaling depends on real sustained CPU, do **not** report autoscaling as observed solely because an HPA YAML exists. Use the optional read-only load generator and measure before/after:
```sh
python scripts/load_test.py --requests 2000 --concurrency 60
kubectl -n food-delivery get hpa -w
```
If CPU remains low and replicas stay at two, record that fact accurately and explain why.

## Step 8 – GitHub: FOUR separate repositories (mandatory)
Create four GitHub repos using the UI, e.g. `quickbite-catalog`, `quickbite-orders`, `quickbite-delivery`, `quickbite-gateway`. For each folder, `cd services/catalog` and run:
```sh
git init
git add .
git commit -m "Implement standalone QuickBite Catalog service"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/quickbite-catalog.git
git push -u origin main
```
Repeat from the respective Orders/Delivery/Gateway directories with each correct remote URL. `git` credentials/authorization are your own. Put the **actual four** links into the report. Optionally create a fifth infra repository containing `docker-compose.yml`, `deploy/`, docs, and tools.

## Step 9 – Final evidence and screen recording
Use `docs/EVIDENCE_CHECKLIST.md` and `docs/DEMO_SCRIPT.md`. Fill student name, ID, member details, links and screenshots in `QuickBite_Assignment_Report.docx`. Record actual code, Postman responses, distinct Docker containers, Minikube deployments, Dashboard and HPA output. Package report, video, source code in `<StudentID>_QuickBite.zip` before 12 Nov 2026; do not submit fabricated screenshots or claimed runtime results.

## Step 10 – Optional GitHub Actions CI/CD
Each service includes `.github/workflows/ci.yml`. After pushing to its own GitHub repository, open GitHub → Actions and verify each independent service workflow ran `pytest` and `docker build` successfully. This is a **CI workflow**; automated deployment/CD requires cluster credentials and should not be claimed without additional setup.
