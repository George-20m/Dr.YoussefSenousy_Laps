# Screenshots

| Screenshot | Description |
|---|---|
| [screenshot_01_containers_running.png](./01_containers_running.png) | All 5 containers running: redis-node1, redis-node2, etcd1, etcd2, etcd3 |
| [screenshot_02_redis_set_master.png](./02_redis_set_master.png) | Writing `SET mykey "hello-from-node1"` on redis-node1 (master) — returns OK |
| [screenshot_03_redis_get_replica.png](./03_redis_get_replica.png) | Reading `GET mykey` on redis-node2 (replica) — returns the value written on master, proving replication works |
| [screenshot_04_redis_replication_info.png](./04_redis_replication_info.png) | `INFO replication` on both nodes — master shows `role:master` with `connected_slaves:1`, replica shows `role:slave` with `master_link_status:up` |
| [screenshot_05_redis_write_during_partition.png](./05_redis_write_during_partition.png) | Writes on redis-node1 while redis-node2 is stopped — both keys return OK, showing master stays available during partition |
| [screenshot_06_redis_eventual_consistency.png](./06_redis_eventual_consistency.png) | Redis-node2 reading `key_during_partition` after restart — returns the value written during partition, proving eventual consistency |
| [screenshot_07_etcd_put.png](./07_etcd_put.png) | `etcdctl put foo bar` on etcd1 — returns OK |
| [screenshot_08_etcd_get.png](./08_etcd_get.png) | `etcdctl get foo` on etcd1 — returns `foo` with value `bar` |
| [screenshot_09_etcd_leader_before.png](./09_etcd_leader_before.png) | `endpoint status --write-out=table` showing the current leader node and its Raft term/index |
| [screenshot_10_etcd_leader_after_failover.png](./10_etcd_leader_after_failover.png) | After killing the leader — new leader elected with a higher Raft term number |
| [screenshot_11_etcd_data_after_failover.png](./11_etcd_data_after_failover.png) | `etcdctl get foo` after failover — data intact, proving Raft guarantees committed entries are never lost |
