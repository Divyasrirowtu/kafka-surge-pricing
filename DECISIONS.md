# DECISIONS.md

## 1. Partitioning Strategy

The `ride-requests` topic is configured with **6 partitions** because the system processes data for **6 distinct city zones**:
- downtown
- airport
- suburbs-north
- suburbs-south
- business-district
- stadium-complex

Each event uses `city_zone` as the message key. Kafka’s default partitioning strategy hashes the key and maps it to a partition. This ensures that all events for a specific zone are always routed to the same partition.

### Why 6 partitions?
- Enables **parallel processing** across consumers
- Ensures **ordering per city zone**, which is critical for accurate surge calculation
- Matches the number of unique keys (zones), allowing balanced distribution

### If fewer partitions (e.g., 2):
- Multiple zones share partitions
- Reduced parallelism
- Possible processing bottlenecks

### If more partitions (e.g., 24):
- Increased overhead on Kafka brokers
- No real benefit since only 6 unique keys exist
- Underutilized partitions

Thus, 6 partitions provide the optimal balance between performance and resource usage.

---

## 2. Consumer Group Design

The system uses **two independent consumer groups**:

1. `pricing-engine-group`
2. `analytics-recorder-group`

Both groups subscribe to the same topic (`ride-requests`) but process data independently.

### Why separate consumer groups?

- **Decoupling of responsibilities**
  - Pricing engine → calculates surge & generates alerts
  - Analytics recorder → aggregates zone statistics

- **Scalability**
  - Each group can scale independently by adding more consumers

- **Fault isolation**
  - Failure in one consumer group does not affect the other

- **Multiple use cases**
  - Same data stream supports different business functions

### Why not a single consumer group?

- Messages would be divided between consumers
- Each service would receive only a subset of data
- Would break independent processing

### Why not a single application?

- Violates microservices principles
- Reduces flexibility and scalability
- Harder to maintain and extend

---

## 3. Offset Commit Strategy

Kafka consumers track progress using offsets. There are two main strategies:

### Auto Commit
- Automatically commits offsets at intervals
- Simple to implement
- Risk: Messages may be marked as processed before actual processing is complete

### Manual Commit
- Offsets are committed only after successful processing
- Ensures higher reliability
- Slightly more complex

### Strategy Used:

#### Pricing Engine Consumer:
- **Manual commit preferred (conceptually)**
- Ensures:
  - Alert is successfully sent to Kafka
  - Data is stored in the database
- Prevents data loss or missed alerts

#### Analytics Recorder Consumer:
- **Auto commit acceptable**
- Occasional data loss is tolerable because:
  - Data is continuously updated
  - Next event will refresh the state

### Trade-off Summary:

| Strategy | Advantage | Disadvantage |
|--------|----------|-------------|
| Auto Commit | Simple | Risk of data loss |
| Manual Commit | Reliable | More complex |

---

## ✅ Conclusion

The system design focuses on:
- Efficient partitioning for scalability
- Independent consumer groups for flexibility
- Reliable offset management for data integrity

These decisions ensure a **highly scalable, fault-tolerant, and real-time event-driven system**, similar to production-grade architectures used in ride-hailing platforms.