# Sepolia ETH Faucet Application

This project is a simple Django-based REST API for a Sepolia testnet ETH faucet. It allows users to receive Sepolia ETH for free from a pre-configured wallet.

## Features

- **Fund Faucet (POST `/faucet/fund`)**: Sends 0.0001 Sepolia ETH from a pre-configured faucet wallet to a given wallet address. Rate-limited to prevent abuse.
- **Faucet Stats (GET `/faucet/stats`)**: Retrieves the number of successful and failed transactions in the last 24 hours.

## Prerequisites

- Python 3.8+
- Django 4.0+
- Docker & Docker Compose (for containerization)
- A Sepolia wallet funded with Sepolia ETH (you can get test ETH from public Sepolia faucets).
- An Infura project (for Web3 provider) – you can create a free account at [Infura.io](https://infura.io/).

## Requirements

 - create a config.py  file in faucet_project
    SEP_ETH_AMOUNT = 0.0001 
    FAUCET_PRIVATE_KEY = ""
    FAUCET_ADDRESS = ""
    WEB3_PROVIDER = ""
    
 - create an empty .env file 

Install project dependencies using `pip`:

```bash
pip install -r requirements.txt
