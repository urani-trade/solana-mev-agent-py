# Aleph: Urani's first in-house MEV Agent in Python

<br>

<p align="center">
<img src="./.internal/mulder_logo.png" width="30%" align="center" style="padding:1px;border:1px solid black;"/>
</p>

<br>

* **[Agent Aleph](https://docs.urani.ag/agents/operator-onboarding/uranis-in-house-agents/mev-agent-aleph)** is Urani's in-house arbitrage agent written in Python.

* Aleph is one of the agents that are always running in the Arena to help with gauging and fallback. Nevertheless, they are not intended to outperform the MEV agents outsourced by operators.

<br>

#### 1. **[Details on how Aleph Works](#how-aleph-works)**
#### 2. **[Entry point: Run Aleph thorugh the CLI](#run-aleph-through-the-cli)**


<br>

----

## How Aleph Works

<br>
1️⃣ Listen for incoming batches: Aleph fetches the orders from the Urani's order book;<br>
2️⃣ Parse these batches to extract the order intents;<br>
3️⃣ Check for peer-to-peer matches among the intents: naive 1-hop search, partial fills are not supported at this time; <br>
4️⃣ Spin a new thread for each intent with no P2P match to calculate solutions for best quotes through arbitrage in different AMMs;<br>
5️⃣ Pack the solutions and send them to the protocol.<br>
<br>

**Note**: Currently, Aleph sends quote requests to [Jupiter](https://station.jup.ag/) to obtain the optimal route for each intent. Future versions will include in-house routing algorithms and fetch AMMs from different venues.

### Aleph's Structure

<br>

Aleph's source code is structured as the following:

* `main.py`: The entry point when running the command line.
* `agents/`: Contains the main classes for the "bots". Also, the entry point for running the agent.
* `solana/`: Contains an extensive wrapper for operations on the Solana blockchain.
* `orders/`: Contains the classes to process intents and batches.
* `liquidity/`: Contains wrapper classes for liquidity venues on the Solana blockchain.
* `p2p/`: Contains algorithms and optimizations for off-chain peer-to-peer matches.
* `protocol_server/`: Contains the API for the local server that mimicks the Urani's protocol.
* `oracles/`: Contain wrapper for price discovery.
* `utils/`: Contains several helper classes and methods for network operations, mathematics, system procedures, oracles, etc. 

<br>

```bash
src
 ├── main.py
 ├── agents
 │   ├── aleph.py
 │   ├── base.py
 │   └── main.py
 ├── liquidity
 │   ├── base.py
 │   ├── cexes
 │   └── jupiter.py
 ├── oracles
 │   ├── dexscreener.py
 │   ├── helius.py
 │   └── pyth.py
 ├── orders
 │   ├── batch.py
 │   ├── intent.py
 │   ├── quote.py
 │   └── solution.py
 ├── p2p
 │   └── level_one.py
 ├── protocol_server
 │   ├── _server.py
 │   ├── order book
 │   ├── server.log
 │   ├── server_utils.py
 │   ├── static
 │   └── templates
 ├── sol
 │   ├── accounts.py
 │   ├── base.py
 │   ├── blocks.py
 │   └── transactions.py
 └── utils
     ├── config.py
     ├── logging.py
     ├── maths.py
     ├── network.py
     └── system.py
```
<br>

----


## Run Aleph through the CLI

### Setup

<br>

Create a `.env` file :
```bash
cp .env.example .env
```

<br>

Fill in the following information:

| Parameter               | Description                   | Default                               |
|-------------------------|-------------------------------|:-------------------------------------:|
| `WALLET_PRIVATE_KEY` | Your private key for signing.    | -                                     |
| `HELIUS_API_KEY`     | Your helius api key              | -                                     |
| `LOG_LEVEL`          | The level of logging you desire. | `info`                                |
| `RPC_HTTPS`          | The RPC HTTP URL to connect.     | `https://api.mainnet-beta.solana.com/`|


<br>

Install the program cli:

```bash
make install
```
### Test the installation 
You can test the installation with 

```bash
poetry run pytest
```

```console
====================================================================== test session starts =======================================================================
platform darwin -- Python 3.12.4, pytest-8.3.2, pluggy-1.5.0
rootdir:  XXX
configfile: pyproject.toml
plugins: order-1.2.1, anyio-4.4.0, ordering-0.6
collected 7 items                                                                                                                                                

tests/test_cli.py ....                                                                                                                                     [ 57%]
tests/test_server.py ..                                                                                                                                    [ 85%]
tests/test_aleph.py .                                                                                                                                      [100%]

======================================================================= 7 passed in 16.25s =======================================================================
```

### CLI commands
You can get information on the CLI commands by running:

```bash
poetry run mcli -h
```

```console
  88       88  8b,dPPYba,  ,adPPYYba,  8b,dPPYba,   88  
  88       88  88P'   "Y8  ""     `Y8  88P'   `"8a  88  
  88       88  88          ,adPPPPP88  88       88  88  
  "8a,   ,a88  88          88,    ,88  88       88  88  
   `"YbbdP'Y8  88          `"8bbdP"Y8  88       88  88        

                                                             
._ _      |  _|  _  ._   ._ _   _        _.  _   _  ._ _|_ 
| | | |_| | (_| (/_ |    | | | (/_ \/   (_| (_| (/_ | | |_ 
                                             _|
                                             
usage: mcli [-h] [-s] [-a [AGENT]] [-d [AGENT]] [-l] [-o]

Mulder CLI: Urani MEV Agent.

options:
  -h, --help            show this help message and exit
  -s                    Print info on the Solana blockchain.
  -a [AGENT], --agents [AGENT]
                        Print info on the available agents or on specific [AGENT]
  -d [AGENT], --deploy [AGENT]
                        Deploy a specific [AGENT].
  -l                    Print info on liquidity sources.
  -o                    Print info on the Oracles.

```

----

### Usage

Aleph is meant to compete with other agents in the Urani Arena, fetching users's intents from the Urani's Protocol order book and posting back its solutions.
This first version of Aleph interacts with a local-server initialized by the user that mimicks the Urani's Protocol order book.

<br>

Start a local server mimicking the Urani's order book

```bash
poetry run start_server
```

This server can be visited at
```bash
http://127.0.0.1:8000/
```

Once the server is running, you can deploy Aleph by running the CLI adding the flag `--deploy` or `-d` and the name of `aleph`:
```bash
poetry run mcli -d aleph

# OR

poetry run python ./src/main.py -d aleph
```

This will output: 
```console


  88       88  8b,dPPYba,  ,adPPYYba,  8b,dPPYba,   88  
  88       88  88P'   "Y8  ""     `Y8  88P'   `"8a  88  
  88       88  88          ,adPPPPP88  88       88  88  
  "8a,   ,a88  88          88,    ,88  88       88  88  
   `"YbbdP'Y8  88          `"8bbdP"Y8  88       88  88        

                                                             
._ _      |  _|  _  ._   ._ _   _        _.  _   _  ._ _|_ 
| | | |_| | (_| (/_ |    | | | (/_ \/   (_| (_| (/_ | | |_ 
                                             _|
                                             
Loading environment variables...

🛹 Deploying Agent Aleph ...
   Aleph is the first Urani MEV in-house agent.
   .Version: v0.1
   .Language: Python
   .Routing algorithm: Jupiter
   .P2P matches: Naive 1-hop
   .Partial fill: No
   .Ring trades: No

   --> Check the README to learn more about Aleph <--

🛹 Starting Agent Aleph...
🛹 Aleph is running...
🛹 Fetching current batch from http://127.0.0.1:8000/batches

⏳ Aleph is waiting for a valid batch ...
```
This means that Aleph is waiting for a batch to be posted in the order book.

To post a valid batch in the order book, open a new terminal window.

Go in the folder `orders_templates`, and post the `order_example.json` via

```@console
curl -X POST "http://127.0.0.1:8000/batches" -H "Content-Type: application/json" -d @example_batch.json
```

Now look what Aleph does:
```console                                                                          


  88       88  8b,dPPYba,  ,adPPYYba,  8b,dPPYba,   88  
  88       88  88P'   "Y8  ""     `Y8  88P'   `"8a  88  
  88       88  88          ,adPPPPP88  88       88  88  
  "8a,   ,a88  88          88,    ,88  88       88  88  
   `"YbbdP'Y8  88          `"8bbdP"Y8  88       88  88        

                                                             
._ _      |  _|  _  ._   ._ _   _        _.  _   _  ._ _|_ 
| | | |_| | (_| (/_ |    | | | (/_ \/   (_| (_| (/_ | | |_ 
                                             _|
                                             
Loading environment variables...

🛹 Deploying Agent Aleph ...
   Aleph is the first Urani MEV in-house agent.
   .Version: v0.1
   .Language: Python
   .Routing algorithm: Jupiter
   .P2P matches: Naive 1-hop
   .Partial fill: No
   .Ring trades: No
   --> Check the README to learn more about Aleph <--

🛹 Starting Agent Aleph...
🛹 Aleph is running...
🛹 Fetching current batch from http://127.0.0.1:8000/batches
⏳ Aleph is waiting for a valid batch ...
🛹 Aleph found a valid batch ...
🤙 Aleph is solving the order...

⚙️  Searching for p2p matches ...
🤙 Found p2p matches.

⚙️  Searching optimal execution path for 2 intents ...
🤙 Sending solutions to http://127.0.0.1:8000/solutions

🛹 Agent Aleph has finished
```

You can check the solutions by visiting: `http://127.0.0.1:8000/solutions`.

If you want to try with another batch, modify the template `orders_templates/order_example.json` as you wish and post it to the order book.
This will override the last batch.

Then run again Aleph.


When you are finished, stop the server with:

```bash
poetry run stop_server
```

<br>

----

## Contributing

You are welcome to contribute. See the guidelines [here](.internal/CONTRIBUTING.md).


