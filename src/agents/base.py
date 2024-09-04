# src/agents/base.py
# Base class for agents

import time

from functools import wraps
from src.orders.batch import BatchData
from src.utils.config import load_config
from src.utils.logging import log_debug, log_info, exit_with_error, hourglass
from src.utils.network import (get_request, post_request, 
                               get_async_request, post_async_request, 
                               html_to_json)

class AgentBase:
    """
    Base class for all agents.

    This class provides common functionality that all agents will inherit,
    such as fetching and posting data, parsing batches, and handling configurations.
    """

    def __init__(self, config=None) -> None:
        self.config = config or load_config()
        
        self.URANI_ORDERBOOK_HTTPS_URL = self.config['URANI_ORDERBOOK_HTTPS_URL']
        self.URANI_ORDERBOOK_WS_URL = self.config['URANI_ORDERBOOK_WS_URL']
        self.URANI_BATCHES_HTTP_ENDPOINT = self.config['URANI_BATCHES_HTTP_ENDPOINT']
        self.URANI_SOLUTION_HTTP_ENDPOINT = self.config['URANI_SOLUTION_HTTP_ENDPOINT']
        self.URANI_BATCHES_SUB_TOPIC = self.config['URANI_BATCHES_SUB_TOPIC']
        self.URANI_SOLUTIONS_SUB_TOPIC = self.config['URANI_SOLUTIONS_SUB_TOPIC']
        
        self.MULDER_UPDATE_SECONDS = self.config['MULDER_UPDATE_SECONDS']
        self.MULDER_MAX_INSTANCES = self.config['MULDER_MAX_INSTANCES']
        self.MULDER_TYPE_OF_CONNECTION = self.config['MULDER_TYPE_OF_CONNECTION'].lower()
        self.batch = BatchData()

    #####################################################
    #                  Private methods
    #####################################################
    @staticmethod
    def initialize_agent(agent_name: str):
        """
        Initialize and return the appropriate agent class based on the agent's name.

        Args:
            agent_name (str): Name of the agent to initialize.

        Returns:
            type: The class of the agent to be instantiated.

        Raises:
            SystemExit: If the agent name is not recognized.
        """
        from src.agents.aleph import Aleph

        # Dictionary mapping agent names to their classes
        agent_classes = {
            "aleph": Aleph
            # Add more agents here as they are developed
        }
        
        # Retrieve the class for the given agent name
        agent_class = agent_classes.get(agent_name.lower())
        
        if agent_class is None:
            exit_with_error(f"No agent found with name: {agent_name}")
        
        return agent_class
    
    #####################################################
    #        Public methods: Retrieving Batches
    #####################################################
    def get_current_batch_http(self) -> dict:
        """
        Retrieve the current batch using HTTP.

        This method continuously attempts to fetch the current batch from URANI's 
        specified HTTP endpoint. If the batch is not found, it waits 1 second and 
        retries until a valid batch is found or the process is interrupted.

        Returns:
            dict: The JSON data of the current batch.

        Raises:
            SystemExit: If an error occurs during the request, or the process is interrupted.
        """
        
        url = self.URANI_ORDERBOOK_HTTPS_URL + self.URANI_BATCHES_HTTP_ENDPOINT
        log_debug(f'Fetching current batch from {url}')
        
        index = 0  # To keep track of which symbol to display
        
        try:
            while True:
                response = get_request(url)
                
                if response.status_code != 200:
                    exit_with_error(f"Error fetching current batch: {response.text}")
                
                json_data = html_to_json(response)
                
                # Check if it is non-empty, if so we have a valid batch
                if json_data: 
                    log_info(f'\n🛹 {self.name} found a valid batch ...')
                    return json_data
                else:
                    index = hourglass(f'{self.name} is waiting for a valid batch ...', index)
                time.sleep(1)

        except KeyboardInterrupt:
            log_info('\n')
            exit_with_error("Process interrupted by the user.\n")

    async def get_current_batch_http_async(self) -> dict:
        """Retrieve the current batch using HTTP asynchronously."""

        url = self.URANI_ORDERBOOK_HTTPS_URL + self.URANI_BATCHES_HTTP_ENDPOINT
        log_debug(f'Fetching current batch from {url}')
        
        index = 0  # To keep track of which symbol to display
        
        try:
            while True:
                response = await get_async_request(url)
                
                if response.status_code != 200:
                    exit_with_error(f"Error fetching current batch: {response.text}")
                
                json_data = html_to_json(response)
                
                # Check if it is non-empty, if so we have a valid batch
                if json_data: 
                    log_info(f'\n🛹 {self.name} found a valid batch ...')
                    return json_data
                else:
                    index = hourglass(f'{self.name} is waiting for a valid batch ...', index)
                time.sleep(1)

        except KeyboardInterrupt:
            log_info('\n')
            exit_with_error("Process interrupted by the user.\n")


    #####################################################
    #        Public methods: Publishing Solutions
    #####################################################

    def post_solution_http(self) -> dict:
        """
        Post the solution using HTTP.

        This method sends the solution data to URANI's specified HTTP endpoint.
        The data is expected to be in a format that `BatchData.solutions_to_dict()`
        returns.

        Raises:
            SystemExit: If unable to post solutions due to a request failure.
        """
        url = self.URANI_ORDERBOOK_HTTPS_URL + self.URANI_SOLUTION_HTTP_ENDPOINT
        solutions = self.batch.solutions_to_dict()
        try: 
            post_request(url, data=solutions)
        except:
            exit_with_error(f"Unable to post solutions to {url}")
    
    async def post_solution_http_async(self, data) -> dict:
        """Post the solution using HTTP asynchronously."""
        
        url = self.URANI_ORDERBOOK_HTTPS_URL + self.URANI_SOLUTION_HTTP_ENDPOINT
        log_debug(f'Posting solution to {url} asynchronously')
        solutions = self.batch.solutions_to_dict()
        try: 
            await post_async_request(url, data=solutions)
        except:
            exit_with_error(f"Unable to post solutions to {url}")

    #####################################################
    #        Public methods: Retrieving Batches
    #####################################################

    def parse_batch(self) -> None:
        """
        Parse the current batch based on the connection type (HTTP/WS).

        This method retrieves the current batch and processes it to extract
        intents and create instances in the `BatchData`.
        """

        if self.MULDER_TYPE_OF_CONNECTION == 'http':
            this_batch = self.get_current_batch_http()
        elif self.MULDER_TYPE_OF_CONNECTION == 'ws':
            this_batch = self.get_current_batch_ws()

        self.batch.batch_id = '1'
        self.batch.parse_intent_instance(this_batch)
    
    async def solve_order(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    async def run(self) -> None:
        """
        Entry point for agents. This method orchestrates the process of retrieving batches,
        solving orders, and posting solutions.

        This is the main method that each agent will call to start its execution.
        """

        log_info(f'🛹 {self.name} is running...')

        # Fetch orders from the Urani's Protocol
        log_info(f'🛹 Fetching current batch from {self.URANI_ORDERBOOK_HTTPS_URL+self.URANI_BATCHES_HTTP_ENDPOINT}\n')
        self.parse_batch()

        # Agent Specific solution: implemented in child class
        await self.solve_order()

        # Post solutions to the Urani's Protocol
        log_info(f'🤙 Sending solutions to {self.URANI_ORDERBOOK_HTTPS_URL+self.URANI_SOLUTION_HTTP_ENDPOINT}')
        self.post_solution_http()
