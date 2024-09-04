# -*- encoding: utf-8 -*-
# src/liquidity/jupiter.py
# Wrapper for Jupiter liquidity source.

from src.utils.network import craft_url
from src.utils.logging import log_debug
from src.liquidity.base import LiquidityBase
from src.orders.intent import IntentData


class JupiterWrapper(LiquidityBase):
    """
    Wrapper for the Jupiter liquidity source.

    This class extends the LiquidityBase class to interact specifically with the
    Jupiter liquidity protocol. It provides methods for configuring the Jupiter
    endpoints, generating quote URLs, and formatting quote data.
    """

    def __init__(self, config=None) -> None:
        """
        Initialize the JupiterWrapper class.

        Args:
            config (dict, optional): Configuration dictionary. If not provided,
                                     the default configuration will be loaded.
        """
        super().__init__(config)

    ###################################################
    #           Private methods for Config
    ###################################################

    def _get_config_data(self) -> None:
        """
        Set the configuration data specific to the Jupiter liquidity source.

        This method overrides the base class implementation to populate the 
        configuration with Jupiter-specific URLs and parameters.
        """
        self.VENUE_URL = self.config['JUPITER_HTTPS']
        self.VENUE_SWAP_ENDPOINT = self.config['JUPITER_SWAP_ENDPOINT']
        self.VENUE_QUOTE_ENDPOINT = self.config['JUPITER_QUOTE_ENDPOINT']

        self.SWAP_RETRIES = self.config['SWAP_RETRIES']
        self.SWAP_SLEEP_TIME = self.config['SWAP_SLEEP_TIME']
        self.ACCEPTABLE_SLIPPAGE = self.config['ACCEPTABLE_SLIPPAGE']

    ###################################################
    #        Private methods for Quotes
    ###################################################

    def get_quote_url(self, intent: IntentData) -> str:
        """
        Construct the URL for retrieving a quote from Jupiter.

        This method builds the full URL required to obtain a quote from the
        Jupiter liquidity protocol using the provided intent data.

        Args:
            intent (IntentData): The intent data containing the necessary
                                 information to build the quote URL.

        Returns:
            str: The fully constructed URL for the quote request.
        """
        quote_endpoint = (self.VENUE_QUOTE_ENDPOINT +
                          '?inputMint=' + intent.source_mint_address +
                          '&outputMint=' + intent.destination_mint_address +
                          '&amount=' + str(intent.source_amount) +
                          '&slippageBps=' + self.ACCEPTABLE_SLIPPAGE)
        log_debug(f'Quote endpoint: {quote_endpoint}')
        return craft_url(self.VENUE_URL, quote_endpoint)

    def get_quote_data(self, quote: dict) -> dict:
        """
        Prepare the data for a quote POST request to Jupiter.

        This method formats the data required to make a POST request to
        Jupiter's quote endpoint, using the provided quote information.

        Args:
            quote (dict): The quote response data received from Jupiter.

        Returns:
            dict: The formatted data ready to be sent in the POST request.
        """
        this_data = {
            "quoteResponse": quote,
            "userPublicKey": str(self.solana.pubkey),
            "wrapUnwrapSOL": True,
        }
        return this_data
