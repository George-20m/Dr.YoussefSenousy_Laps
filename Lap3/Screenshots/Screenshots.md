# Screenshots

| Screenshot | Description |
|---|---|
| [01-namespaces-cgroups.png](./01-namespaces-cgroups.png) | Interactive Ubuntu container showing `hostname`, `ps -ef`, `ip addr`, `mount | head`, and `cat /proc/1/cgroup` to demonstrate namespace and cgroup isolation |
| [02-pid-namespace-comparison.png](./02-pid-namespace-comparison.png) | Side-by-side comparison of the container process view and the host PID of the same container process, showing PID namespace isolation |
| [03-cgroups-limits.png](./03-cgroups-limits.png) | `docker stats` output while running `stress` in a limited container, showing CPU capped near `0.5` and memory constrained near `256 MB` |
| [04-basic-image-history.png](./04-basic-image-history.png) | `docker history lab3-basic` and image listing for the basic single-stage Docker image |
| [05-image-comparison.png](./05-image-comparison.png) | Comparison of `lab3-basic` and `lab3-multi` in `docker image ls`, used to compare image size and layering |
| [06-kubernetes-cluster.png](./06-kubernetes-cluster.png) | `kubectl get nodes -o wide` showing the local kind cluster node in `Ready` state |
| [07-kubernetes-pods-running.png](./07-kubernetes-pods-running.png) | `kubectl get pods -o wide` showing all 3 `lab3-web` Pods in `Running` state |
| [08-service-curl-test.png](./08-service-curl-test.png) | Successful `curl` requests to `/` and `/health` through the forwarded Kubernetes service |
| [09-node-labels.png](./09-node-labels.png) | `kubectl get nodes --show-labels` showing the applied `node-role=general` label |
| [10-pods-with-node-selector.png](./10-pods-with-node-selector.png) | Pod listing after reapplying the Deployment with `nodeSelector`, confirming scheduling against the labeled node |
| [11-pod-self-healing.png](./11-pod-self-healing.png) | `kubectl get pods -w` showing a deleted Pod terminating and a replacement Pod being created to restore the desired replica count |
| [12-probes-configured.png](./12-probes-configured.png) | `kubectl describe pod` output showing readiness and liveness probe configuration and related events |
| [13-container-restart.png](./13-container-restart.png) | `kubectl get pods -w` showing the Pod staying the same while the container `RESTARTS` counter increments after killing PID 1 |
