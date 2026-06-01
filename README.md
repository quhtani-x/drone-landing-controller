# Autonomous Drone Landing (PID control)

A drone falls under gravity and gets blown around by random wind. A set of PID
controllers figure out the thrust and tilt needed to keep it level and bring it
down gently onto the landing pad. Drag the pad with your mouse and the drone
chases it and lands.

This is the same kind of control loop a real quadcopter flight controller runs.

## what's inside

- a reusable `PID` class (proportional + integral + derivative, with anti-windup)
- one PID for horizontal position, one for descent rate, one to keep it level
- simple physics: thrust vs gravity + random wind gusts
- "soft landing" only counts if the touchdown speed is low enough

## run

```bash
pip install pygame
python sim.py
```

tags: ai, control, pid, drones, simulation, pygame, robotics

PID controllers are everywhere in robotics, wanted to feel how tuning them works.
