# Buddy System
A Pi Pico-based LoRa two-way communication system designed to improve safety on haul roads. Integrates GPS to inform compatible devices of the device's location.

## Status
Alpha; devices communicate with each other and return range values. Output is via terminal and other transmission elements are not implemented.

## Current goals
 1. Rework Rx/Tx loop to make Rx non-blocking
 2. Improve LoRa range in software config; potentially upgrade hardware
 3. Develop minimalistic encoding for coordinates and additional transmission data
 4. Integrate hardware I/O