# -*- encoding: utf-8 -*-
# src/oracles/helius.py
# Wrapper for Helius price source.

from src.utils.network import post_request
from src.utils.logging import log_error, log_info


class HeliusWrapper:
    """
    Wrapper for Helius price source.

    This class provides methods to interact with the Helius API to fetch
    current prices for specified tokens.
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize the HeliusWrapper with configuration settings.

        Args:
            config (dict): Configuration dictionary containing Helius RPC URL and API key.
        """
        self.config = config
        self.url = self.config['HELIUS_RPC_HTTPS']
        self.api = self.config['HELIUS_API_KEY']

    #######################################################
    #                 Public methods
    #######################################################

    def get_price_token(self, token_address: str) -> float:
        """
        Get the current price of a specified token from Helius.

        This method fetches the price of the given token address from Helius's API.

        Args:
            token_address (str): The address of the token to get the price for.

        Returns:
            float: The current price of the token.

        Raises:
            Exception: If there is an error with the API request or data parsing, it logs the error.
        """
        url = f"{self.url}?api-key={self.api}"
        data = {
            "jsonrpc": "2.0",
            "id": "my-id",
            "method": "getAsset",
            "params": {
                "id": token_address,
                "displayOptions": {
                    "showFungible": True
                }
            },
        }

        log_info(f'Fetching price for token {token_address} on Helius...')
        response = post_request(url, data=data)

        try:
            return response['result']['token_info']['price_info']['price_per_token']
        except Exception as e:
            log_error(f"Error fetching price for {token_address} on Helius: {e}")
            return 0
