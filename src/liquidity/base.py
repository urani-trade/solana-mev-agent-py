# -*- encoding: utf-8 -*-
# src/liquidity/base.py
# Base class for liquidity sources.

from src.orders.intent import IntentData
from src.utils.config import load_config
from src.utils.logging import log_debug
from src.utils.network import get_async_request
from src.sol.transactions import SolanaTransactions


class LiquidityBase:
    """
    Base class for all liquidity sources.

    This class provides the foundation for interacting with various liquidity venues.
    It handles configuration, transaction setup, and basic functionality that specific
    liquidity sources will extend.
    """

    def __init__(self, config: dict = None) -> None:
        """
        Initialize the LiquidityBase class.

        This constructor sets up the configuration, transaction handling, and basic
        attributes required for interacting with a liquidity venue.

        Args:
            config (dict, optional): Configuration dictionary. If not provided, 
                                     the default configuration will be loaded.
        """
        self.config = config or load_config()

        self.VENUE_URL = None
        self.VENUE_QUOTE_ENDPOINT = None
        self.VENUE_SWAP_ENDPOINT = None

        self.SWAP_RETRIES = None
        self.SWAP_SLEEP_TIME = None
        self.ACCEPTABLE_SLIPPAGE = None

        self.solana = SolanaTransactions(config=self.config, is_async=False)
        self._get_config_data()

        assert self.VENUE_URL is not None, \
                    'Please fill in venue URL in _get_config_data().'
        assert self.VENUE_QUOTE_ENDPOINT is not None, \
                    'Please fill in quote endpoint in _get_config_data().'
        assert self.VENUE_SWAP_ENDPOINT is not None, \
                    'Please fill in swap endpoint in _get_config_data().'

        log_debug(f'\nInitializing {self.__class__.__name__}...')
        log_debug(f'Liquidity venue: {self.VENUE_URL}')
        log_debug(f'Acceptable slippage: {self.ACCEPTABLE_SLIPPAGE}')

    ###################################################
    #           Private methods for Config
    ###################################################

    def _get_config_data(self) -> None:
        """
        Populate the configuration with the necessary values.

        This method is intended to be overridden by child classes to set the
        specific venue URLs and endpoints required for quoting and swapping.
        """
        self.VENUE_URL = None
        self.VENUE_QUOTE_ENDPOINT = None
        self.VENUE_SWAP_ENDPOINT = None

        self.ACCEPTABLE_SLIPPAGE = self.config['ACCEPTABLE_SLIPPAGE']
        self.SWAP_RETRIES = self.config['SWAP_RETRIES']
        self.SWAP_SLEEP_TIME = self.config['SWAP_SLEEP_TIME']

    ###################################################
    #        Private methods for Quotes
    ###################################################

    def get_quote_url(self, intent: IntentData = None) -> str:
        """
        Construct the URL for retrieving a quote.

        This method should be implemented in child classes. It builds the full URL
        for the quote endpoint, potentially using information from the provided intent.

        Args:
            intent (IntentData, optional): The intent data used to customize the quote URL.

        Returns:
            str: The fully constructed quote URL.
        """
        pass

    def get_quote_data(self, quote: dict) -> dict:
        """
        Prepare the data for a quote request.

        This method should be implemented in child classes. It fills in the necessary
        values required for making a POST request to obtain a quote from the liquidity venue.

        Args:
            quote (dict): The raw quote data to be processed.

        Returns:
            dict: The processed quote data ready for the POST request.
        """
        pass

    async def get_quote(self, intent: IntentData) -> dict:
        """
        Retrieve the quote for the specified intent.

        This method creates a quote request using the provided intent and sends it to
        the liquidity venue's quote endpoint.

        Args:
            intent (IntentData): The intent data used to generate the quote.

        Returns:
            dict: The response data containing the quote.
        """
        quote_url = self.get_quote_url(intent)
        log_debug(f'\nCreating quote for {intent.intent_id} at {quote_url}...')
        return await get_async_request(quote_url)
