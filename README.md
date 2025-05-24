#  Heist Challenge Solver – TryHackMe

A Python script to exploit a vulnerable Ethereum smart contract in the TryHackMe **Heist** room.

##  Features

- Fetches challenge data via the API
- Takes contract ownership
- Withdraws ETH from the contract
- Verifies if the challenge is solved
- (Optional) Tries to fetch the flag

## ⚙️ Requirements

```bash
pip install web3 requests
