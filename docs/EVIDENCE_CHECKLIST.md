# Evidence capture checklist — do not mark an item complete until tested on your laptop

- [ ] E01: architecture diagram and service ownership table (provided as design material)
- [ ] E02: code/repository roots (`catalog`, `orders`, `delivery`, `gateway`)
- [ ] E03: GET restaurants Postman request and 200 JSON response
- [ ] E04: GET menu Postman request and 200 JSON response
- [ ] E05: POST order (201) with server total 2997 cents for m1×2+m3×1
- [ ] E06: GET order and list orders (200)
- [ ] E07: POST delivery 201, GET delivery 200, repeated POST 409
- [ ] E08: `pytest -q` and `python scripts/smoke_test.py` passing
- [ ] E09: `docker compose ps` showing six containers and health status
- [ ] E10: `kubectl -n food-delivery get pods,deploy,svc,pvc` and ready replica counts
- [ ] E11: Minikube dashboard showing namespace `food-delivery` / actual Deployments
- [ ] E12: Kubernetes HPA / `kubectl top pods`; clearly distinguish configured target from observed scale-out
- [ ] E13: GitHub pages showing FOUR separate service repositories
- [ ] E14: test measurements from optional load generator (before/after) if performed
- [ ] E15: demo recording showing deployment and working APIs; save recording as a real MP4

Document each screenshot with: Figure ID, command/API, result, and a one-line explanation. Replace report placeholders only with genuine observations.
