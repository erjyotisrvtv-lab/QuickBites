# QuickBite examiner demo script (5–8 minutes; adapt to actual results)

**00:00 – Introduction:** “Hello, I am [name], student ID [ID]. This is my SEZG583 Scalable Services assignment titled QuickBite: Microservices Development and Deployment.”

**00:30 – Design:** “Our application separates restaurant/menu discovery, order placement, and delivery tracking into independently owned services. The gateway is the single customer-facing entry point. Orders owns its database, and Delivery owns a different database. Services collaborate over REST, not direct database access.” Show `docs/architecture_diagram.png`.

**01:30 – Commands and queries:** Show the operations table in the assignment report. GET operations query catalog/orders/delivery; POST operations create orders and deliveries.

**02:00 – Implementations:** Open the four service directories. Highlight Catalog menu, Orders server-side price calculation, Delivery order validation + uniqueness, and Gateway routing. Show local health checks and docs.

**03:00 – Live Postman APIs:** Show GET restaurants, GET menu, POST order, GET order, POST delivery, GET delivery. Show invalid menu item 422 and duplicate delivery 409. Use the supplied Postman collection.

**04:15 – Docker:** Show `docker compose ps`, six separate containers, logs, and the gateway’s web UI. State which containers are APIs and which are PostgreSQL databases.

**05:15 – Kubernetes:** Show Minikube status, `kubectl -n food-delivery get deployments,statefulset,pods,svc,pvc`, Dashboard Namespace = food-delivery. Explain two application replicas, HPA CPU 70%, 2–10 bound and resource requests/limits. If load was tested, show genuine observed HPA results; otherwise say scale-out was configured and not demonstrated.

**06:30 – GitHub:** Show 4 separate repository pages and README files. Mention independent build/deploy/test artifacts.

**07:00 – Conclusion:** “The assignment demonstrates design, microservice implementation, independent container deployment, Kubernetes orchestration, service discovery, availability checks, and scalable application-tier configuration. Production database failover and payment processing are future scope.”
