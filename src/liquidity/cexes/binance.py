# -*- encoding: utf-8 -*-
# src/liquidity/cexes/binance.py
# Wrapper for Binance price source and trading.

from src.utils.network import get_request
from src.utils.logging import log_error, log_info


class BinanceWrapper:
    """
    Wrapper for Binance price source and trading.

    This class provides methods to interact with the Binance API to fetch 
    current prices for specified tokens.
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize the BinanceWrapper with configuration settings.

        Args:
            config (dict): Configuration dictionary containing Binance API URL.
        """
        self.config = config
        self.url = self.config['BINANCE_HTTPS']

    #######################################################
    #                 Public methods
    #######################################################

    def get_price_token(self, token_symbol: str) -> float:
        """
        Get the current price of a specified token on Binance.

        This method fetches the price of the given token symbol against USDT 
        from Binance's API.

        Args:
            token_symbol (str): The symbol of the token to get the price for.

        Returns:
            float: The current price of the token in USDT.

        Raises:
            Exception: If there is an error with the API request, it logs the error.
        """
        token_url = f"{self.url}{token_symbol}USDT"
        log_info(f'Fetching price for token {token_symbol} on Binance...')
        
        response = get_request(token_url)
        
        if response.status_code != 200:
            log_error(f"Error fetching price for {token_symbol} on Binance: {response.text}")
            raise Exception(f"Failed to fetch price for {token_symbol}")
        else:
            return float(response.json()['price'])
