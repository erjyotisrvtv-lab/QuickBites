# QuickBite — BITS Pilani SEZG583 Scalable Services

**Main project repository:** This repository contains the complete source for all four microservices. Clone this repository once; separate service repositories are not required to run the application.

| Component | Source in this repository |
|---|---|
| Catalog | [services/catalog](services/catalog/) |
| Orders | [services/orders](services/orders/) |
| Delivery | [services/delivery](services/delivery/) |
| Gateway and UI | [services/gateway](services/gateway/) |
| Kubernetes manifests | [deploy/kubernetes](deploy/kubernetes/) |
| Docker Compose | [docker-compose.yml](docker-compose.yml) |
| Postman collection | [postman](postman/) |
| Documentation | [docs](docs/) |

Each service retains its own source, dependencies, Dockerfile and tests, so it can be built and deployed independently from this shared repository. The existing separate service repositories remain available; they are not required dependencies or Git submodules.

**Scope:** Part 1 design; Part 2 four standalone independently deployable Python/FastAPI microservices; Part 3 Docker Compose, Minikube Kubernetes and Dashboard; submission documentation and demo instructions.

**Start here:** `docs/STEP_BY_STEP_EXECUTION.md` (Windows/macOS commands). See `docs/ARCHITECTURE.md` and `docs/EVIDENCE_CHECKLIST.md`.

```
services/catalog/         Standalone FastAPI Catalog source; port 3001, in-memory demo data
services/orders/          Standalone FastAPI Orders source; port 3002, own Orders DB
services/delivery/        Standalone FastAPI Delivery source; port 3003, own Delivery DB
services/gateway/         Standalone FastAPI Gateway source + browser UI; port 8080
deploy/kubernetes/        Namespace, secret example, Postgres, Deployments, Services, HPA, PDB
postman/                  Importable Postman collection
scripts/                  End-to-end smoke and read-only load tests
tests/                    Python pytest source tests
docs/                     Architecture, step-by-step, evidence checklist, demo script
run_local.py              Starts 4 processes in SQLite local mode without Docker
docker-compose.yml        Starts 4 microservice containers + 2 PostgreSQL containers
QuickBite_Assignment_Report.docx   Editable assignment report
```

## Quick launch without Docker
```sh
python -m pip install -r requirements-dev.txt
python run_local.py
# in a second terminal
python scripts/smoke_test.py
pytest -q
```
Browser `http://127.0.0.1:8080`.

## Docker
`docker compose up --build -d`, then `docker compose ps`.

## Kubernetes
See step 6 of docs/STEP_BY_STEP_EXECUTION.md. Minikube/Docker must be installed and actually running; YAML files alone do not prove a deployment.

## Academic notes
Reconstructed as an original educational implementation **based on supplied screenshots**, not a byte-exact copy of their source. The uploaded zip held screenshots rather than readable code files. Review and adapt the code before submission. No GitHub repository was created by this bundle; no screenshot or deployment result is represented as actual runtime evidence. Demonstrate and cite only your own work. Demo DB credentials must never be reused for any real deployment.

## Optional CI/CD (assignment extra)
The active repository workflow is [QuickBite Microservices CI](.github/workflows/quickbite-ci.yml): it runs the root automated tests and builds all four service images. Its deployment job requires the configured Windows self-hosted runner and an existing Minikube deployment. Workflow files inside individual service folders are retained for standalone repository use; GitHub Actions does not discover them as workflows in this repository.
