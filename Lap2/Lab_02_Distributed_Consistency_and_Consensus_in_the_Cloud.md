# Lab 02 – Distributed Consistency and Consensus in the Cloud

## Lab Description

This lab explores how distributed systems handle consistency, availability, and consensus. Two tools are used: **Redis** (to demonstrate replication and eventual consistency) and **etcd** (to explore the Raft consensus protocol).

---

## File Structure

| File | Description |
|------|-------------|
| `Lab_02_Distributed_Consistency_and_Consensus_in_the_Cloud.md` | This file — describes the lab and contains reflection answers |
| `docker-compose.yml` | Starts 5 containers: redis-node1, redis-node2, etcd1, etcd2, etcd3 |
| `Screenshots.md` | Links and descriptions for all 11 screenshots |
| `screenshots/` | 11 screenshots documenting the lab steps |

---

## Screenshots

See [Screenshots.md](./Screenshots/Screenshots.md) for all screenshots with descriptions.

---

## Reflection Answers

**Q1: What is eventual consistency and how did you observe it with Redis?**

Eventual consistency means that after a write, all replicas will eventually reflect that value — but not immediately. When redis-node2 was stopped, writes continued on redis-node1. When node2 came back online, Redis automatically synced the missed writes. For a period, node2 had stale data — that is eventual consistency. The system prioritized availability and corrected consistency later.

**Q2: What is the Raft consensus algorithm and why does etcd use it?**

Raft is a consensus protocol that makes a cluster of nodes agree on a sequence of values even if some nodes crash. It elects one leader who handles all writes and replicates them to followers. A write is only committed once a majority (quorum) confirms receipt. etcd uses Raft because it needs strong consistency — Kubernetes relies on etcd for cluster state, so it cannot tolerate stale reads or lost writes.

**Q3: What happened to the etcd cluster when you stopped the leader?**

The two remaining followers detected that the leader stopped sending heartbeats. After an election timeout, one became a candidate, requested votes from the other, and was elected the new leader. The Raft term number incremented. When the old leader came back, it saw the higher term and automatically stepped down to become a follower.

**Q4: What does CAP theorem say, and which side does each system fall on?**

CAP theorem states that a distributed system can guarantee at most two of three properties: Consistency, Availability, and Partition Tolerance.

Redis (master-replica) prioritizes Availability + Partition Tolerance (AP) — it stays available during a partition and accepts stale reads on replicas.

etcd prioritizes Consistency + Partition Tolerance (CP) — if the cluster loses quorum, it refuses writes rather than risk inconsistency.
