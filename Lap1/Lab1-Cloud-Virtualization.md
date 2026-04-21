# Lab 1: Exploring Cloud Virtualization and Data Center Architecture

## Lab Description

This lab explores cloud virtualization technologies through three parts: comparing Virtual Machines (VMs) and Containers, examining AWS cloud infrastructure architecture, and simulating tail latency behavior in distributed systems.

---

## File Structure

| File | Description |
|------|-------------|
| `Lab1-Cloud-Virtualization.md` | This file — describes the lab and key concepts |
| `app.py` | Flask application with exponential delay simulation |
| `load_test.py` | Load testing script with concurrency options |
| `Screenshots.md` | Links and descriptions for all 6 screenshots |
| `screenshots/` | 6 screenshots documenting the lab results |

---

## Screenshots

See [Screenshots.md](./Screenshots/Screenshots.md) for all screenshots with descriptions.

---

## Key Concepts Covered
- Containers are lightweight (shared kernel, <1s startup, ~4 processes)
- VMs provide strong isolation (separate kernel, 10-30s startup, 97 processes)
- Use VMs for strong isolation, different OS kernels, or legacy apps
- Use containers for microservices, CI/CD, and high-density deployments

**AWS Nitro Hypervisor**
- AWS Nitro offloads networking, storage, and management to dedicated hardware
- This improves performance and security compared to traditional hypervisors
- EC2 instances expose block devices as NVMe drives via direct hardware passthrough
- Instance metadata is accessible at 169.254.169.254

**Tail Latency**
- P99 latency was ~21% higher than the mean in our tests
- Higher concurrency increases tail latency variance
- At 100 parallel requests, there is a 63.4% probability that at least one request exceeds P99
- Tail latency compounds in microservices chains — if Service A calls B which calls C, each with P99=100ms, the chain's P99 could be 300ms+