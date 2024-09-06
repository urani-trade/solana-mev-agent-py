## MEV Agent Aleph

<br>

<p align="center">
<img src="https://github.com/user-attachments/assets/78cb883e-8ba4-4a63-8f67-1f33f4a827bf" width="20%" align="center" style="padding:1px;border:1px solid black;"/>
</p>



<br>

#### 👉🏼 [Agent Aleph](https://docs.urani.trade/mev-agents/agents) is Urani's in-house arbitrage agent written in Python. Although the private version of Aleph is private for the Urani Protocol, this template brings its basic proprieties to the public.

#### 👉🏼 Authors: **[bt3gl](https://github.com/von-steinkirch)** and **[luca-nik](https://github.com/luca-nik)**.

#### 👉🏼 **[Details on how the public version of Aleph v0.1 works](#how-aleph-works)**.
#### 👉🏼 **[Details on how to run Aleph thorugh its CLI](#run-aleph-through-the-cli)**.


<br>

----

## How Aleph Works

<br>

1️⃣ Listen for incoming batches: Aleph fetches the orders from the Urani's orderbook;<br>
2️⃣ Parse these batches to extract the order intents;<br>
3️⃣ Check for peer-to-peer matches among the intents: naive 1-hop search, partial fills are not supported at this time; <br>
4️⃣ Spin a new thread for each intent with no P2P match to calculate solutions for best quotes through arbitrage in different AMMs;<br>
5️⃣ Pack the solutions and send them to the protocol.<br>

<br>

For this particular release, we bring an example of Aleph sending quote requests to **[Jupiter](https://station.jup.ag/)** to obtain the optimal route for each intent. Future versions will expand routing algorithms and fetch AMMs from different venues.

<br>

---

### Aleph's Structure

<br>

Aleph's source code is structured as the following:

* `main.py`: The entry point when running the command line.
* `agents/`: Contains the main classes for the "bots". Also, the entry point for running the agent.
* `solana/`: Contains an extensive wrapper for operations on the Solana blockchain.
* `orders/`: Contains the classes to process intents and batches.
* `liquidity/`: Contains wrapper classes for liquidity venues on the Solana blockchain.
* `p2p/`: Contains algorithms and optimizations for off-chain peer-to-peer matches.
* `protocol_server/`: Contains the API for the local server that mimick the Urani protocol.
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
 │   ├── orderbook
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

<br>

### Local Setup

<br>

Create a `.env` file :

```bash
cp .env.example .env
vim .env
```

<br>

Fill in the following information:

| Parameter               | Description                      | Default                               |
|-------------------------|----------------------------------|:-------------------------------------:|
| `WALLET_PRIVATE_KEY`    | Your private key for signing.    | -                                     |
| `HELIUS_API_KEY`        | Your helius api key              | -                                     |
| `LOG_LEVEL`             | The level of logging you desire. | `info`                                |
| `RPC_HTTPS`             | The RPC HTTP URL to connect.     | `https://api.mainnet-beta.solana.com/`|


<br>

Install the program cli:

```bash
make install
```

<br>

---

### Test the installation 

<br>

You can test the installation with:

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

<br>

---

### Running the CLI

<br>

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


Aleph CLI: Urani MEV Agent.

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

<br>

----

### Usage

<br>

This first version of Aleph interacts with a local-server initialized by the user that mimics the Urani Protocol.

<br>

Start a local server:

```bash
poetry run start_server
```

<br>

This server can be visited at:

```bash
http://127.0.0.1:8000/
```

<br>

Once the server is running, you can deploy Aleph by running the CLI, adding the flag `--deploy` or `-d` and the string `aleph`:

```bash
poetry run mcli -d aleph

# OR

poetry run python ./src/main.py -d aleph
```

<br>

This will output: 

```console


  88       88  8b,dPPYba,  ,adPPYYba,  8b,dPPYba,   88  
  88       88  88P'   "Y8  ""     `Y8  88P'   `"8a  88  
  88       88  88          ,adPPPPP88  88       88  88  
  "8a,   ,a88  88          88,    ,88  88       88  88  
   `"YbbdP'Y8  88          `"8bbdP"Y8  88       88  88        
                                             
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

<br>

This means Aleph is waiting for a batch to be posted in the orderbook. 
To post a valid batch in the orderbook, open a new terminal window and go into the folder `orders_templates`. 
Post post the `order_example.json` via:

```@console
curl -X POST "http://127.0.0.1:8000/batches" -H "Content-Type: application/json" -d @example_batch.json
```

<br>

Now look what Aleph does:

```console                                                                          


  88       88  8b,dPPYba,  ,adPPYYba,  8b,dPPYba,   88  
  88       88  88P'   "Y8  ""     `Y8  88P'   `"8a  88  
  88       88  88          ,adPPPPP88  88       88  88  
  "8a,   ,a88  88          88,    ,88  88       88  88  
   `"YbbdP'Y8  88          `"8bbdP"Y8  88       88  88        

                                                             
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

<br>

You can check the solutions by visiting: `http://127.0.0.1:8000/solutions`.

If you want to try with another batch, modify the template `orders_templates/order_example.json` as you wish and post it to the orderbook.
This will override the last batch.

Then run again Aleph.

When you are finished, stop the server with:

```bash
poetry run stop_server
```

<br>


---

### License and Contributing

<br>

This project is distributed under the **[Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0)**. 

You are welcome to contribute. See the guidelines **[here](.internal/CONTRIBUTING.md)**.

<br>
