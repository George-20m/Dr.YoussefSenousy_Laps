# Screenshots

Interactive Ubuntu container showing `hostname`, `ps -ef`, `ip addr`, `mount | head`, and `cat /proc/1/cgroup` to demonstrate namespace and cgroup isolation.

![01-namespaces-cgroups](./01-namespaces-cgroups.png)

Figure: `01-namespaces-cgroups.png`

---

Side-by-side comparison of the container process view and the host PID of the same container process, showing PID namespace isolation.

![02-pid-namespace-comparison](./02-pid-namespace-comparison.png)

Figure: `02-pid-namespace-comparison.png`

---

`docker stats` output while running `stress` in a limited container, showing CPU capped near `0.5` and memory constrained near `256 MB`.

![03-cgroups-limits](./03-cgroups-limits.png)

Figure: `03-cgroups-limits.png`

---

`docker history lab3-basic` and image listing for the basic single-stage Docker image.

![04-basic-image-history](./04-basic-image-history.png)

Figure: `04-basic-image-history.png`

---

Comparison of `lab3-basic` and `lab3-multi` in `docker image ls`, used to compare image size and layering.

![05-image-comparison](./05-image-comparison.png)

Figure: `05-image-comparison.png`

---

`kubectl get nodes -o wide` showing the local kind cluster node in `Ready` state.

![06-kubernetes-cluster](./06-kubernetes-cluster.png)

Figure: `06-kubernetes-cluster.png`

---

`kubectl get pods -o wide` showing all 3 `lab3-web` Pods in `Running` state.

![07-kubernetes-pods-running](./07-kubernetes-pods-running.png)

Figure: `07-kubernetes-pods-running.png`

---

Successful `curl` requests to `/` and `/health` through the forwarded Kubernetes service.

![08-service-curl-test](./08-service-curl-test.png)

Figure: `08-service-curl-test.png`

---

`kubectl get nodes --show-labels` showing the applied `node-role=general` label.

![09-node-labels](./09-node-labels.png)

Figure: `09-node-labels.png`

---

Pod listing after reapplying the Deployment with `nodeSelector`, confirming scheduling against the labeled node.

![10-pods-with-node-selector](./10-pods-with-node-selector.png)

Figure: `10-pods-with-node-selector.png`

---

`kubectl get pods -w` showing a deleted Pod terminating and a replacement Pod being created to restore the desired replica count.

![11-pod-self-healing](./11-pod-self-healing.png)

Figure: `11-pod-self-healing.png`

---

`kubectl describe pod` output showing readiness and liveness probe configuration and related events.

![12-probes-configured](./12-probes-configured.png)

Figure: `12-probes-configured.png`

---

`kubectl get pods -w` showing the Pod staying the same while the container `RESTARTS` counter increments after killing PID 1.

![13-container-restart](./13-container-restart.png)

Figure: `13-container-restart.png`
