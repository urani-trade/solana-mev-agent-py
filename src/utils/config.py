# -*- encoding: utf-8 -*-
# src/utils/config.py
# Helper for configuring the system.


import os

from pathlib import Path
from dotenv import load_dotenv

from src.utils.system import open_json
from src.utils.logging import exit_with_error, set_logging


def load_config() -> dict:
    """
        Load and set environment variables.
        You only need to modify this function if you
        add new environment variables.
    """

    config_file = Path('.') / '.env'
    if not os.path.isfile(config_file):
        exit_with_error('Please create an .env file')

    config = {}
    load_dotenv(config_file)

    # Secrets
    config['WALLET_PRIVATE_KEY'] = os.getenv('WALLET_PRIVATE_KEY')
    config['HELIUS_API_KEY'] = os.getenv('HELIUS_API_KEY')

    # General config
    config['LOG_LEVEL'] = os.getenv('LOG_LEVEL')
    config['SOLANA_NETWORK'] = os.getenv('SOLANA_NETWORK')
    config['SOLANA_RPC_HTTPS'] = os.getenv('SOLANA_RPC_HTTPS')
    config['TX_EXPLORER'] = os.getenv('TX_EXPLORER')
    config['URANI_ORDERBOOK_HTTPS_URL'] = os.getenv('URANI_ORDERBOOK_HTTPS_URL')
    config['URANI_ORDERBOOK_WS_URL'] = os.getenv('URANI_ORDERBOOK_WS_URL')
    config['URANI_BATCHES_HTTP_ENDPOINT'] = os.getenv('URANI_BATCHES_HTTP_ENDPOINT')
    config['URANI_SOLUTION_HTTP_ENDPOINT'] = os.getenv('URANI_SOLUTION_HTTP_ENDPOINT')
    config['URANI_BATCHES_SUB_TOPIC'] = os.getenv('URANI_BATCHES_SUB_TOPIC')
    config['URANI_SOLUTIONS_SUB_TOPIC'] = os.getenv('URANI_SOLUTIONS_SUB_TOPIC')

    # Mulder
    config['MULDER_TYPE_OF_CONNECTION'] = os.getenv('MULDER_TYPE_OF_CONNECTION')
    config['MULDER_UPDATE_SECONDS'] = int(os.getenv('MULDER_UPDATE_SECONDS'))
    config['MULDER_MAX_INSTANCES'] = int(os.getenv('MULDER_MAX_INSTANCES'))

    # Liquidity Providers Endpoints
    config['JUPITER_HTTPS'] = os.getenv('JUPITER_HTTPS')
    config['ZETA_HTTPS'] = os.getenv('ZETA_HTTPS')
    config['RAYDIUM_HTTPS'] = os.getenv('RAYDIUM_HTTPS')
    config['PHOENIX_HTTPS'] = os.getenv('PHOENIX_HTTPS')
    config['ORCA_HTTPS'] = os.getenv('ORCA_HTTPS')
    config['METEORA_HTTPS'] = os.getenv('METEORA_HTTPS')
    config['LIFINITY_HTTPS'] = os.getenv('LIFINITY_HTTPS')
    config['DRIFT_HTTPS'] = os.getenv('DRIFT_HTTPS')
    config['ARCANA_HTTPS'] = os.getenv('ARCANA_HTTPS')

    # Liquiduty Providers Endpoints
    config['JUPITER_SWAP_ENDPOINT'] = os.getenv('JUPITER_SWAP_ENDPOINT')
    config['ZETA_SWAP_ENDPOINT'] = os.getenv('ZETA_SWAP_ENDPOINT')
    config['RAYDIUM_SWAP_ENDPOINT'] = os.getenv('RAYDIUM_SWAP_ENDPOINT')
    config['PHOENIX_SWAP_ENDPOINT'] = os.getenv('PHOENIX_SWAP_ENDPOINT')
    config['ORCA_SWAP_ENDPOINT'] = os.getenv('ORCA_SWAP_ENDPOINT')
    config['METEORA_SWAP_ENDPOINT'] = os.getenv('METEORA_SWAP_ENDPOINT')
    config['LIFINITY_SWAP_ENDPOINT'] = os.getenv('LIFINITY_SWAP_ENDPOINT')
    config['DRIFT_SWAP_ENDPOINT'] = os.getenv('DRIFT_SWAP_ENDPOINT')
    config['ARCANA_SWAP_ENDPOINT'] = os.getenv('ARCANA_SWAP_ENDPOINT')

    config['JUPITER_QUOTE_ENDPOINT'] = os.getenv('JUPITER_QUOTE_ENDPOINT')
    config['ZETA_QUOTE_ENDPOINT'] = os.getenv('ZETA_QUOTE_ENDPOINT')
    config['RAYDIUM_QUOTE_ENDPOINT'] = os.getenv('RAYDIUM_QUOTE_ENDPOINT')
    config['PHOENIX_QUOTE_ENDPOINT'] = os.getenv('PHOENIX_QUOTE_ENDPOINT')
    config['ORCA_QUOTE_ENDPOINT'] = os.getenv('ORCA_QUOTE_ENDPOINT')
    config['METEORA_QUOTE_ENDPOINT'] = os.getenv('METEORA_QUOTE_ENDPOINT')
    config['LIFINITY_QUOTE_ENDPOINT'] = os.getenv('LIFINITY_QUOTE_ENDPOINT')
    config['DRIFT_QUOTE_ENDPOINT'] = os.getenv('DRIFT_QUOTE_ENDPOINT')
    config['ARCANA_QUOTE_ENDPOINT'] = os.getenv('ARCANA_QUOTE_ENDPOINT')

    # Oracle and other Endpoints
    config['HELIUS_RPC_HTTPS'] = os.getenv('HELIUS_RPC_HTTPS')
    config['DEXSCREENER_HTTPS'] = os.getenv('DEXSCREENER_HTTPS')
    config['BINANCE_HTTPS'] = os.getenv('BINANCE_HTTPS')

    # System and  Mint IDs
    config['TOKEN_PROGRAM_ID'] = os.getenv('TOKEN_PROGRAM_ID')
    config['SOL_MINT'] = os.getenv('SOL_MINT')
    config['USDC_MINT'] = os.getenv('USDC_MINT')
    config['USDT_MINT'] = os.getenv('USDT_MINT')
    config['JUP_MINT'] = os.getenv('JUP_MINT')
    config['JITO_MINT'] = os.getenv('JITO_MINT')

    # Internal
    config['LOGO_FILE'] = os.getenv('LOGO_FILE')
    config['SPACER_FILE'] = os.getenv('SPACER_FILE')
    config['WEBSOCKET_DELAY'] = os.getenv('WEBSOCKET_DELAY')
    config['WEBSOCKET_TIMEOUT'] = os.getenv('WEBSOCKET_TIMEOUT')
    config['RATE_LIMIT_MAX_RETRIES'] = os.getenv('RATE_LIMIT_MAX_RETRIES')
    config['RATE_LIMIT_DELAY'] = os.getenv('RATE_LIMIT_DELAY')
    config['SWAP_RETRIES'] = os.getenv('SWAP_RETRIES')
    config['SWAP_SLEEP_TIME'] = os.getenv('SWAP_SLEEP_TIME')
    config['ACCEPTABLE_SLIPPAGE'] = os.getenv('ACCEPTABLE_SLIPPAGE')
    config['COMPUTER_UNIT_PRICE'] = os.getenv('COMPUTER_UNIT_PRICE')

    # Check for missing values
    for key, value in config.items():
        if value is None:
            exit_with_error(f'Please set {key} in the .env file. Exiting.')

    assert config['SOLANA_NETWORK'] in ['mainnet', 'devnet', 'testnet']
    assert config['MULDER_TYPE_OF_CONNECTION'] in ['HTTP', 'WS', 'ASYNC_HTTP', 'PUBSUB']
    assert config['LOG_LEVEL'] in ['info', 'error', 'debug']

    set_logging(config['LOG_LEVEL'])
    return config
