---
title: "Seat Domain Model API"
description: "Comprehensive seat domain model with hierarchical components and capabilities"
---

# Seat Domain Model API

The Seat Domain Model API provides a comprehensive hierarchical structure for vehicle seat systems. This GraphQL API demonstrates the seat domain with nested components including backrest, headrest, seating surface, and complete capability controls.

## Domain Structure

- **Hierarchical Components**: Seat → Backrest → Headrest → Seating Surface
- **Position Control**: Precise positioning on x, y, and z axes
- **Comfort Features**: Heating, cooling, and massage systems
- **Occupancy Detection**: Real-time monitoring and safety integration
- **VSS Compliance**: Aligned with Vehicle Signal Specification standards

## Key Components

### Seat Positioning
- Linear position adjustment (front/back)
- Height adjustment (up/down)
- Tilt angle control

### Comfort Controls
- Heating and cooling systems (-100% to +100%)
- Multi-level massage functionality (0-100%)
- Lumbar support adjustment
- Side bolster control

### Safety Features
- Occupancy detection
- Seatbelt position monitoring
- Airbag deployment status

## Example Operations

Query seat domain structure, control positions, and manage comfort features through the GraphQL playground above.
