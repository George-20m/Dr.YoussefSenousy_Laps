# Lab 4 - Microservices and Cloud-Native Design

## Lab Description

This lab implements a small cloud-native e-commerce backend using two Python Flask microservices and Docker Compose. The work focuses on service separation, synchronous service-to-service communication, container packaging, environment-based configuration, health checks, restart behavior, and basic resilience under failure.

---

## File Structure

| File | Description |
|------|-------------|
| `Lap4_Microservices_and_Cloud_Native_Design.md` | This file - describes the lab, summarizes the implementation, and contains reflection answers |
| `docker-compose.yml` | Defines the two services, port mappings, environment variables, health checks, and restart policies |
| `product-service/app.py` | Flask microservice exposing `/health` and `/products/<product_id>` |
| `product-service/requirements.txt` | Python dependencies for `product-service` |
| `product-service/Dockerfile` | Docker image build instructions for `product-service` |
| `order-service/app.py` | Flask microservice exposing `/health` and `/orders`, and calling `product-service` synchronously |
| `order-service/requirements.txt` | Python dependencies for `order-service` |
| `order-service/Dockerfile` | Docker image build instructions for `order-service` |
| `Screenshots/Screenshots.md` | Links and descriptions for all screenshots |
| `Screenshots/` | Screenshots documenting the lab results |

---

## Screenshots

See [Screenshots.md](./Screenshots/Screenshots.md) for all screenshots with descriptions.

---

## Implementation Summary

The system is split into two independent services:

- `product-service` stores a small in-memory product catalog and returns product data as JSON.
- `order-service` accepts order requests, contacts `product-service` to validate the product, and returns an order summary.

Both services are containerized separately using Docker, which reflects the microservice principle of independent packaging and deployment. Docker Compose is used to run both containers together, provide service discovery by container name, and manage startup, health checks, and restart policy.

The `order-service` reads the `PRODUCT_SERVICE_URL` from an environment variable rather than hardcoding the address. This matches cloud-native configuration practice and keeps the service portable across environments.

To improve resilience, `order-service` uses a request timeout and retry loop when calling `product-service`. This does not remove the dependency, but it helps the service fail more gracefully when the downstream service is unavailable.

---

## Reflection Answers

**Q1: Which parts of this lab show the benefits of microservices over a monolith?**

The system is divided into `product-service` and `order-service`, each with a single clear responsibility. Each service has its own code, dependencies, Dockerfile, and container, which makes deployment more modular. This separation improves maintainability and makes it easier to scale or replace one service without redesigning the whole application.

**Q2: Which new complexities were introduced by splitting the system into two services?**

The split introduces network communication, service discovery, port management, health checks, and failure handling between services. Instead of a direct function call inside one application, `order-service` must make HTTP requests to `product-service`, handle timeouts, and deal with unavailable dependencies. Container orchestration also becomes part of the system design.

**Q3: What would break if network latency increased or one service became slow?**

Since `order-service` depends synchronously on `product-service`, slower network calls would delay order creation. If `product-service` became too slow or stopped responding, `order-service` would eventually timeout and return an error to the client. This demonstrates how latency and availability problems propagate through synchronous microservice chains.

**Q4: Which 12-factor app principles are visible in this implementation?**

- Configuration is separated from code through the `PRODUCT_SERVICE_URL` environment variable.
- Each service is packaged as a disposable container image and can be started or restarted independently.
- Logs are emitted to standard output by the Flask applications and can be viewed with `docker compose logs`.
- The services are stateless for this lab because no local persistent files are required for runtime operation.

---

## Key Concepts Covered

- Microservices separate responsibilities into independently deployable services
- Dockerfiles package each service into its own container image
- Docker Compose provides local orchestration and service-to-service networking
- Health endpoints support observability and operational checks
- Environment variables make service configuration portable
- Synchronous calls create coupling, so downstream failure can affect upstream behavior
- Timeout and retry improve graceful failure handling, but they do not eliminate dependency risk
