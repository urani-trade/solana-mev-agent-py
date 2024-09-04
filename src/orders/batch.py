# -*- encoding: utf-8 -*-
# src/orders/batch.py
# This class implements an API to parse order batches.

from src.orders.intent import IntentData
from src.utils.logging import exit_with_error, pprint


class BatchData:
    """
    A class to handle and parse order batches.

    This class manages order batches by parsing JSON data into intents,
    converting solutions to a dictionary, and providing methods to access 
    and print solutions.
    """

    def __init__(self) -> None:
        """
        Initialize the BatchData instance.

        Sets up initial attributes for batch_id, intents, solutions, and AMMs.
        """
        self.batch_id = None
        self.intents = []
        self.solutions = {}
        self.amms = None

    ###########################
    #     Access methods      #
    ###########################

    @property
    def print_solutions(self) -> None:
        """
        Pretty print full solutions data.

        This property uses the `pprint` function to display the `solutions` attribute
        in a readable format.
        """
        pprint(self.solutions)

    def solutions_to_dict(self) -> dict:
        """
        Convert the list of solutions belonging to the batch into a dictionary.

        Returns:
            dict: A dictionary where each key is a solution ID and each value is
                  the dictionary representation of the corresponding solution.
        """
        return {key: solution.to_dict() for key, solution in self.solutions.items()}

    ###############################
    #     Public methods          #
    ###############################

    def parse_intent_instance(self, input_json: dict) -> None:
        """
        Parse a batch of orders from a JSON input into a list of intents.

        This method processes the input JSON to extract orders and converts them
        into `IntentData` instances, appending them to the `intents` attribute.

        Args:
            input_json (dict): JSON data containing orders. Expected format includes a key "orders"
                               with a dictionary of intents, where each intent is represented as a dictionary.

        Raises:
            Exception: If there is an error parsing any intent, it logs the error and stops processing.
        """
        orders = input_json.get("orders", {})
        for intent_id, intent_data in orders.items():
            try:
                self.intents.append(IntentData(**intent_data))
            except Exception as e:
                exit_with_error(f"Could not parse intent {intent_data.get('intentId', 'unknown')}: {e}")
