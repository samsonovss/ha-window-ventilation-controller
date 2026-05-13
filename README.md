# PID Window Controller

Custom Home Assistant integration for controlling a window/cover by PID.

## Features

- Select an indoor temperature sensor in the UI
- Select the controlled cover/window in the UI
- Optional outdoor temperature sensor
- PID control of cover position from 0–100%
- Adjustable target temperature and PID coefficients
- Optional summer/winter logic based on outdoor temperature

## Status

This is an initial HACS-ready version focused on the core PID controller.

## Installation

### HACS

1. Open HACS.
2. Add this repository as a custom integration repository.
3. Install **PID Window Controller**.
4. Restart Home Assistant.
5. Go to **Settings → Devices & services → Add integration**.
6. Select the indoor temperature sensor and the target cover.

### Manual installation

Copy `custom_components/pid_window` to `/config/custom_components/pid_window` and restart Home Assistant.

## Entities

- `switch` to enable/disable the controller
- `number` helpers for target temperature and PID coefficients
- `sensor` entities for controller state and live values
- `button` for recalculating helper values / tuning hooks

## Notes

- The component is designed for a window with 0–100% position control.
- The outdoor sensor is optional.
- If the outdoor sensor is present, it can be used to limit window opening in warm weather.
