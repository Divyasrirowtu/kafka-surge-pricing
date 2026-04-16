# DECISIONS.md

## 1. Partitioning Strategy
The `ride-requests` topic is created with 6 partitions because there are 6 distinct city zones:
- downtown
- airport
- suburbs-north
- suburbs-south
- business-district
- stadium-complex

Each zone is used as the message key, ensuring that all events for a specific zone go to the same partition. This guarantees ordering and allows parallel processing.

If fewer partitions (e.g., 2) were used, it would reduce parallelism and create bottlenecks. If more partitions (e.g., 24) were used, it would increase overhead without significant benefit since only 6 keys exist.

---

## 2. Consumer Group Design
Two separate consumer groups are used:
- pricing-engine
- analytics-recorder

This allows both services to independently consume the same data stream without interfering with each other. It supports scalability and separation of concerns.

Using a single consumer group would prevent independent processing, and combining both logics in one service would reduce flexibility.

---

## 3. Offset Commit Strategy
Manual offset commit is preferred for the pricing-engine to ensure messages are processed successfully before committing.

For analytics-recorder, auto-commit can be acceptable since occasional data loss is tolerable.

Manual commit reduces the risk of data loss but adds complexity, while auto-commit is simpler but less reliable.