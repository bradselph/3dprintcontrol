# Ender 3 Control GUI - User Guide

## Overview

This application provides a graphical interface for controlling your Ender 3 3D printer. The interface is divided into several sections for different printer functions.

## Getting Started

1. Connect your Ender 3 printer to your computer via USB
2. Launch the application
3. The software will automatically attempt to connect to the printer
4. A success message will appear if connection is successful

## Interface Sections

### Movement Controls
- Directional arrows for X/Y movement
- Z↑ and Z↓ buttons for Z-axis control
- All movements use the selected step size

### Step Size Control
- Choose movement distance from dropdown:
  - 0.1mm
  - 1mm
  - 10mm
  - 50mm
  - 100mm

### Temperature Controls
- Hotend temperature control (0-250°C)
- Bed temperature control (0-100°C)
- Use "Set" buttons to apply temperature changes

### Status Display
- Shows current temperatures for hotend and bed
- Displays current X, Y, and Z positions
- Updates every second

### Homing Controls
- Home All: Homes all axes
- Home X: Homes X axis only
- Home Y: Homes Y axis only
- Home Z: Homes Z axis only

## Troubleshooting

### Connection Issues
- Ensure printer is powered on
- Check USB connection
- Verify CH340 driver is installed
- Use "Test Connection" button to verify communication

### Temperature Control
- Allow sufficient time for heating/cooling
- Monitor current temperature in status display
- If temperature isn't changing, check printer power

### Movement Issues
- Ensure printer is homed before movement
- Check if motors are enabled
- Verify step size selection

## Safety Notes

- Monitor printer during operation
- Do not leave heated printer unattended
- Ensure proper cooling before shutdown
- Keep printer firmware updated