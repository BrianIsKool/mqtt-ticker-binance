# Binance Ticker to MQTT Publisher

## Description

This Python script connects to Binance's API, retrieves real-time market data, and publishes this data to an MQTT broker. It listens to price changes for trading pairs that involve USDT (Tether) and sends updates to the MQTT topic for each trading pair. The script is built using the `binance` API, `paho.mqtt` library, and asyncio for asynchronous operations.

The bot monitors Binance system status and ensures that the process is kept alive by restarting if it becomes unresponsive for more than a minute.

## Features

- Connects to Binance and listens to `miniTicker` streams for all USDT pairs.
- Publishes the latest ticker prices to an MQTT broker.
- System status monitoring with automatic process restart if the system becomes unresponsive.
- Uses asynchronous programming to manage multiple tasks concurrently.

## Requirements

- Python 3.7 or higher
- Binance API keys (public and secret)
- MQTT broker details (host, port)
- Libraries: `binance`, `paho-mqtt`, `asyncio`
