# -*- encoding: utf-8 -*-
# src/oracles/pyth.py
# Wrapper for Pyth oracle source.

from pythclient.utils import get_key
from pythclient.pythclient import PythClient
from src.utils.logging import log_debug, log_error, log_info, pprint


class PythWrapper:
    """
    Wrapper for Pyth oracle source.

    This class provides methods to interact with the Pyth API to fetch
    current prices for specified tokens.
    """

    def __init__(self, config: dict) -> None:
        """
        Initialize the PythWrapper with configuration settings.

        Args:
            config (dict): Configuration dictionary containing Solana network settings and Pyth client keys.
        """
        self.network = config['SOLANA_NETWORK']
        self.config = config
        self.client = PythClient(
            first_mapping_account_key=get_key(self.network, 'mapping'),
            program_key=get_key(self.network, 'program')
        )

    ########################################################
    #                 Public methods                       #
    ########################################################

    async def get_pyth_prices(self) -> dict:
        """
        Get the current Pyth prices for all products.

        This method fetches the prices of all products from the Pyth API
        and returns them in a dictionary format.

        Returns:
            dict: A dictionary containing the symbols, keys, descriptions, aggregate prices, and confidence intervals
                  for all products.

        Raises:
            Exception: If there is an error fetching or parsing the prices, it logs the error.
        """
        results = {}
        async with self.client as c:
            await c.refresh_all_prices()
            products = await c.get_products()

            for p in products:
                prices = await p.get_prices()

                for _, pr in prices.items():
                    try:
                        key = str(pr.product.key)
                        symbol = pr.product.attrs['generic_symbol']
                        description = pr.product.attrs['description']
                        log_debug(f'Printing for {symbol}')

                        if pr.aggregate_price is not None:
                            log_debug(f'{symbol} has no price.')

                        results[symbol] = {
                            "symbol": symbol,
                            "key": key,
                            "description": description,
                            "aggregate price": pr.aggregate_price,
                            "confidence interval": pr.aggregate_price_confidence_interval,
                        }
                    except Exception as e:
                        log_debug(f"Error: {e}")

        return results

    async def get_pyth_price_for_token_symbol(self, token_symbol: str) -> float:
        """
        Get the current price of a specific token from Pyth.

        This method fetches the price of a specified token symbol from Pyth's API.

        Args:
            token_symbol (str): The symbol of the token to get the price for.

        Returns:
            float: The current price of the token.

        Raises:
            Exception: If there is an error fetching or parsing the price, it logs the error.
        """
        async with self.client as c:
            try:
                await c.refresh_all_prices()
                products = await c.get_products()

                for p in products:
                    prices = await p.get_prices()

                    for _, pr in prices.items():
                        try:
                            symbol = pr.product.attrs['generic_symbol']
                            if symbol == token_symbol:
                                return pr.aggregate_price
                        except Exception as e:
                            log_debug(f"Error: {e}")
            except Exception as e:
                log_error(f"Error fetching price for {token_symbol} on Pyth: {e}")

    async def get_price_token(self, token_symbol: str) -> float:
        """
        Get the price of a specified token from Pyth.

        This method fetches the price of the given token symbol, suffixed with 'USD', from Pyth's API.

        Args:
            token_symbol (str): The symbol of the token to get the price for.

        Returns:
            float: The current price of the token in USD.

        Raises:
            Exception: If no price is found for the token, it logs an error.
        """
        token_symbol_pyth = f'{token_symbol}USD'
        log_info(f'Fetching price for token {token_symbol_pyth} on Pyth...')

        result = await self.get_pyth_price_for_token_symbol(token_symbol_pyth)
        if result is None:
            log_error(f'No price found for {token_symbol_pyth}.')

        return result

    ########################################################
    #                 Print helper methods                #
    ########################################################

    async def print_current_prices(self) -> None:
        """
        Print the current prices in a readable format.

        This method fetches and prints the prices for all products from Pyth.
        """
        results = await self.get_pyth_prices()
        pprint(results)
