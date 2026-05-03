# Lab 5 - Local Serverless Computing and Event-Driven Architectures

## Lab Description

This lab implements a local serverless-style event-driven image processing pipeline using Docker Compose, Redis Streams, Python, Flask, and Pillow. The objective is to simulate core serverless concepts such as event sources, event routers, event destinations, function-style processing, fan-out routing, and cold-start behavior without using any cloud provider.

---

## File Structure

| File | Description |
|------|-------------|
| `Lab5_Local_Serverless_Computing.md` | This file - describes the lab, summarizes the implementation, and contains reflection answers |
| `docker-compose.yml` | Defines Redis, event-source, event-router, image-resizer, and notifier services |
| `event_source/watcher.py` | Watches the input folder and publishes events to Redis Streams |
| `router/event_router.py` | Reads events from Redis and routes them to destination functions |
| `functions/image_resizer/app.py` | Receives image event, resizes image, saves output |
| `functions/notifier/app.py` | Receives event and logs notification message |
| `data/input/` | Input folder for uploaded test images |
| `data/output/` | Output folder for processed images |
| `Screenshots/Screenshots.md` | Links and descriptions for screenshots |
| `Screenshots/` | All screenshots used in submission |

---

## Screenshots

See [Screenshots.md](./Screenshots/Screenshots.md) for screenshot descriptions.

---

## Implementation Summary

The system is composed of five local services:

- `redis` acts as the event/message bus using Redis Streams.
- `event-source` watches the `/data/input` folder for new images.
- `event-router` reads published events and routes them to functions.
- `image-resizer` behaves like a serverless function that resizes uploaded images.
- `notifier` behaves like a second function that logs notifications.

When a new image is placed in the input folder:

1. The event source detects the file.
2. An `image.uploaded` event is published to Redis Streams.
3. The router consumes the event.
4. The router sends the same event to two destinations:
   - image-resizer
   - notifier
5. The resized image is saved in `/data/output`.

This demonstrates event-driven fan-out architecture.

---

## Cold-Start Measurement Table

| Measurement | Value |
|------------|------|
| Warm request time | 483.90 ms |
| First request after restart | 136.98 ms |
| Difference | 346.92 ms faster after restart |
| Reason / explanation | Local timing can vary due to Docker caching, host performance, dependency loading, and OS scheduling. This local experiment simulates startup behavior but may not exactly match real cloud cold starts. |

---

## Reflection Answers

**Q1: What is the event source in this lab?**

The event source is `watcher.py`, which monitors the `/data/input` folder and detects newly added image files. When a file is detected, it creates and publishes an event.

---

**Q2: What is the event router?**

The event router is `event_router.py`. It reads events from Redis Streams and forwards them to the correct destination services based on event type.

---

**Q3: What are the event destinations?**

The event destinations are:

- `image-resizer`
- `notifier`

These functions receive the event and perform processing.

---

**Q4: Why is this pipeline loosely coupled?**

Each service is independent and communicates through events rather than direct hardcoded dependencies. This allows services to be modified, replaced, or scaled separately.

---

**Q5: What happened after restarting the image-resizer container?**

After restarting the container, the first request behaved differently in timing compared with the warm request. This demonstrates startup effects after container initialization.

---

**Q6: How is this similar to serverless cold start?**

Real serverless platforms may take longer for the first request after inactivity because the runtime must initialize. Restarting the container locally demonstrates a similar concept.

---

**Q7: What is missing compared with real cloud serverless platforms?**

This local lab does not include:

- Automatic scaling
- Pay-per-use billing
- Managed monitoring
- IAM/security integration
- Global deployment
- Fully ephemeral runtime execution

---

**Q8: How could this pipeline be extended to support image moderation, OCR, or ML enrichment?**

Additional functions could subscribe to the same event stream, such as:

- OCR text extraction
- NSFW / moderation scanning
- Face detection
- Object recognition
- AI tagging / metadata enrichment

---

## Key Concepts Covered

- Event-driven architecture
- Event source / event router / event destinations
- Redis Streams as a local event bus
- Fan-out event processing
- Function-style container services
- Docker Compose orchestration
- Local simulation of serverless cold starts
- Loosely coupled distributed design