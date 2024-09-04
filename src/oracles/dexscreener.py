# -*- encoding: utf-8 -*-
# src/oracles/dexscreener.py
# Wrapper for Dexscreener price source.

from src.utils.network import get_request, craft_url
from src.utils.logging import log_error, log_info


class DexscreenerWrapper:
    """
    Wrapper for Dexscreener price source.

    This class provides methods to interact with the Dexscreener API to fetch
    current prices for specified tokens.
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize the DexscreenerWrapper with configuration settings.

        Args:
            config (dict): Configuration dictionary containing Dexscreener API URL and other settings.
        """
        self.config = config
        self.url = self.config['DEXSCREENER_HTTPS']

    #######################################################
    #                 Public methods
    #######################################################

    def get_price_token(self, token_address: str, token_symbol: str) -> float:
        """
        Get the current price of a specified token on Dexscreener.

        This method fetches the price of the given token symbol from Dexscreener's API.
        It returns the price in USD and defaults to the first available pair if the preferred pair is not found.

        Args:
            token_address (str): The address of the token to get the price for.
            token_symbol (str): The symbol of the token to get the price for.

        Returns:
            float: The current price of the token in USD.

        Raises:
            Exception: If there is an error with the API request or data parsing, it logs the error.
        """
        token_url = craft_url(self.url, token_address)
        log_info(f'Fetching price for token {token_symbol} on Dexscreener...')
        
        response = get_request(token_url)

        if response.status_code != 200:
            log_error(f"Error fetching price for {token_symbol} on Dexscreener: {response.text}")
            return 0

        response = response.json()

        try:
            for pair in response['pairs']:
                if pair['quoteToken']['address'] == self.config['SOL_MINT']:
                    return pair['priceUsd']
            return response['pairs'][0]['priceUsd']
        except Exception as e:
            log_error(f"Error parsing price for {token_symbol} on Dexscreener: {e}")
            return 0
