# Creating NPCs with Different Behaviors

## Overview
NPCs in Tokyo Times use a configuration-based system that separates behavior from code. Each NPC can have different personalities by using different configs.

## Quick Start

### Using Pre-defined Configs

```python
from entities.npc import NPC
from entities.npc_configs import HENRY_CONFIG, ACTIVE_CONFIG, LAZY_CONFIG, EXPLORER_CONFIG

# Create Henry (default behavior - balanced)
henry = NPC(x=100, y=200, game=game, config=HENRY_CONFIG)

# Create an active NPC that wanders a lot
active_npc = NPC(x=300, y=200, game=game, config=ACTIVE_CONFIG)

# Create a lazy NPC that mostly idles
lazy_npc = NPC(x=500, y=200, game=game, config=LAZY_CONFIG)

# Create an explorer that loves to travel between scenes
explorer = NPC(x=700, y=200, game=game, config=EXPLORER_CONFIG)
```

### Creating Custom Configs

```python
from entities.npc_configs import NPCConfig

# Create a custom shopkeeper config
SHOPKEEPER_CONFIG = NPCConfig(
    name="Shopkeeper",
    idle_min_duration=3.0,
    idle_max_duration=8.0,
    wander_probability=0.40,  # 40% chance to wander (check shop)
    travel_probability=0.0,   # Never leaves the shop
    # 60% chance to idle again (stays behind counter)
    wander_radius=150.0,      # Small wander area
    speed=80.0,               # Slow movement
)

shopkeeper = NPC(x=400, y=300, game=game, config=SHOPKEEPER_CONFIG)
```

## Configuration Parameters

### Idle State
- `idle_min_duration`: Minimum time (seconds) to stay idle
- `idle_max_duration`: Maximum time (seconds) to stay idle

### State Transitions (from Idle)
- `wander_probability`: Chance to start wandering (0.0 to 1.0)
- `travel_probability`: Chance to travel to another scene (0.0 to 1.0)
- Idle again probability is calculated as: `1.0 - wander - travel`

### Wander State
- `wander_radius`: Maximum distance (pixels) to wander from current position
- `wander_portal_min_distance`: Minimum distance (pixels) to stay away from portals
- `max_wander_time`: Maximum time (seconds) to spend wandering before giving up

### Travel State
- `max_travel_time`: Maximum time (seconds) to spend traveling before giving up

### Movement
- `speed`: Movement speed in pixels per second

## Pre-defined Configs

### HENRY_CONFIG (Balanced)
- Idles for 2-5 seconds
- 65% wander, 10% travel, 25% idle again
- Wander radius: 200px, Speed: 100px/s

### ACTIVE_CONFIG (Energetic)
- Idles for 1-3 seconds
- 80% wander, 5% travel, 15% idle again
- Wander radius: 300px, Speed: 150px/s

### LAZY_CONFIG (Sluggish)
- Idles for 5-10 seconds
- 30% wander, 5% travel, 65% idle again
- Wander radius: 100px, Speed: 50px/s

### EXPLORER_CONFIG (Adventurous)
- Idles for 1-2 seconds
- 40% wander, 50% travel, 10% idle again
- Wander radius: 250px, Speed: 120px/s

## Examples

### Guard NPC (Stays in one area)
```python
GUARD_CONFIG = NPCConfig(
    name="Guard",
    idle_min_duration=4.0,
    idle_max_duration=6.0,
    wander_probability=0.20,  # Occasional patrol
    travel_probability=0.0,   # Never leaves post
    wander_radius=100.0,      # Small patrol area
    speed=60.0,
)
```

### Messenger NPC (Constantly moving between scenes)
```python
MESSENGER_CONFIG = NPCConfig(
    name="Messenger",
    idle_min_duration=0.5,
    idle_max_duration=1.0,
    wander_probability=0.20,
    travel_probability=0.70,  # Loves to travel!
    wander_radius=150.0,
    speed=140.0,
)
```

### Customer NPC (Explores shop, sometimes leaves)
```python
CUSTOMER_CONFIG = NPCConfig(
    name="Customer",
    idle_min_duration=2.0,
    idle_max_duration=4.0,
    wander_probability=0.60,  # Browsing
    travel_probability=0.20,  # Sometimes leaves
    wander_radius=250.0,
    speed=90.0,
)
```
