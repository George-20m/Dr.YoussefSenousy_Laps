# Lab 03 - Containerization and Cluster Orchestration

## Lab Description

This lab explores container isolation, Docker image layering, and local Kubernetes orchestration using `kind`. The work is divided into five parts: observing namespaces and cgroups, comparing Docker image builds, deploying a replicated Flask app to Kubernetes, constraining scheduling with labels and selectors, and examining Kubernetes self-healing with health probes.

---

## File Structure

| File | Description |
|------|-------------|
| `Lap3_CMC.md` | This file - describes the lab, summarizes observations, and contains reflection answers |
| `app.py` | Flask application exposing `/` and `/health` |
| `requirements.txt` | Python dependency list for the Flask app |
| `Dockerfile.basic` | Single-stage Docker image build |
| `Dockerfile.multistage` | Multi-stage Docker image build |
| `deployment.yaml` | Kubernetes Deployment for `lab3-web` with 3 replicas and `nodeSelector` |
| `service.yaml` | ClusterIP Service exposing the deployment internally |
| `probe-deployment.yaml` | Kubernetes Deployment with readiness and liveness probes |
| `Screenshots/Screenshots.md` | Links and descriptions for all 13 screenshots |
| `Screenshots/` | 13 screenshots documenting the lab results |

---

## Screenshots

See [Screenshots.md](./Screenshots/Screenshots.md) for all screenshots with descriptions.

---

## Docker Image Comparison

| Aspect | `lab3-basic` | `lab3-multi` |
|------|------|------|
| Build style | Single-stage build | Multi-stage build |
| Base runtime | `python:3.12-slim` | `python:3.12-slim` |
| Observed image size | `199 MB` | `184 MB` |
| Observed history entries | `16` | `15` |
| Dependency install | Installed directly into the final image | Installed in a builder stage, then copied into the final stage |
| Caching when only `app.py` changes | `requirements.txt` and `pip install` layers stay cached | Builder stage stays cached; only final `COPY app.py` layer changes |
| Expected effect | Simple and direct build | Cleaner separation between build and runtime stages |

---

## Reflection Answers

**Q1: Why does the container think its main process is PID 1 while the host sees a different PID? Explain the role of the PID namespace.**

The container has its own PID namespace, so process numbering starts from its isolated view. Inside the container the main process appears as PID 1, while the host assigns it a different real PID.

**Q2: How do cgroups complement namespaces?**

Namespaces isolate what a process can see, but they do not limit resource usage. cgroups add CPU and memory limits so one container cannot consume everything on the host.

**Q3: Which image is smaller and why?**

`lab3-multi` is smaller: `184 MB` versus `199 MB` for `lab3-basic`. The multi-stage build keeps only what is needed in the final runtime image.

**Q4: Which steps are cached if only `app.py` changes?**

The dependency layers stay cached because `requirements.txt` does not change. Only the `COPY app.py` step and anything after it need rebuilding.

**Q5: Why does layer order matter?**

Docker reuses layers from top to bottom. Putting stable steps first avoids reinstalling dependencies on every small code change.

**Q6: Why is using a node selector different from hard-coding a machine name in traditional deployment models? How does declarative scheduling improve resilience and maintainability?**

A node selector targets node labels, not one exact machine. This makes scheduling more flexible and easier to maintain if infrastructure changes.

**Q7: Why is Pod replacement after deletion called reconciliation rather than simple restart logic?**

Kubernetes compares the actual cluster state with the desired state and acts to close the gap. That continuous control loop is reconciliation.

**Q8: Did Kubernetes restart the container in place or create a brand-new Pod after killing PID 1? Explain the difference based on what you observe.**

Kubernetes restarted the container in place inside the same Pod. The Pod name stayed the same and the `RESTARTS` count increased.

**Q9: Why do namespaces alone not guarantee fair resource use?**

Namespaces isolate visibility only. Without cgroups, a container could still consume too much CPU or memory.

**Q10: How do cgroups improve cluster stability?**

cgroups prevent one container from exhausting shared host resources. That keeps other containers and the node itself more stable.

**Q11: Why is Docker image layering important for large-scale orchestration?**

Layers are cached and shared, which reduces build time, storage use, and image transfer cost across many deployments.

**Q12: What does Kubernetes mean by "desired state"?**

Desired state is the target configuration declared in YAML, such as replica count, image, labels, and probes. Kubernetes works continuously to make reality match that declaration.

**Q13: How is self-healing different from traditional manual operations?**

Traditional operations depend on a human noticing and fixing failures. Kubernetes detects failures automatically and recovers based on the declared configuration.

**Q14: Why are readiness probes and liveness probes not interchangeable?**

Readiness controls whether a Pod receives traffic, while liveness controls whether the container should be restarted. They solve different problems.

**Q15: What is one limitation of observing scheduling in a single-node kind cluster compared with a real multi-node cluster?**

A single-node cluster cannot show real placement tradeoffs across multiple nodes. You can verify labels and selectors, but not true scheduling choices or failover behavior.
