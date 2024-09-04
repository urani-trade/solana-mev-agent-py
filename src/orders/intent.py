# -*- encoding: utf-8 -*-
# src/orders/intent.py
# This module defines the IntentData class, which models an intent for an agent in the system.
# The class is used to represent the details of an intent, including source and destination token information.

from dataclasses import dataclass


@dataclass
class IntentData:
    """
    Represents a user's intent for token transfer.

    This class models the details of an intent, including information about the source and destination tokens,
    their respective addresses, amounts, and other relevant details.
    """

    intent_id: str
    source_token: str
    source_mint_address: str
    source_address: str
    source_amount: int
    source_token_decimals: int
    destination_token: str
    destination_mint_address: str
    destination_address: str
    destination_token_decimals: int
    min_receive_amount: int
    partial_fill: bool
    expiration: int
    status: str

    def __init__(self, 
                 intent_id: str, 
                 source_token: str, 
                 source_mint_address: str, 
                 source_address: str, 
                 source_amount: int, 
                 destination_token: str, 
                 destination_mint_address: str,
                 destination_address: str,
                 min_receive_amount: int, 
                 partial_fill: bool,
                 expiration: int, 
                 status: str,
                 source_token_decimals: int,
                 destination_token_decimals: int):
        """
        Initialize the IntentData instance.

        Args:
            intent_id (str): Unique identifier for the intent.
            source_token (str): Token type at the source.
            source_mint_address (str): Mint address of the source token.
            source_address (str): Address from which the source token is being transferred.
            source_amount (int): Amount of source token to be transferred.
            destination_token (str): Token type at the destination.
            destination_mint_address (str): Mint address of the destination token.
            destination_address (str): Address to which the destination token is being transferred.
            min_receive_amount (int): Minimum amount of destination token expected to be received.
            expiration (int): Expiration timestamp of the intent.
            partial_fill (bool): Indicates if the order can be partially filled.
            status (str): Current status of the intent.
            source_token_decimals (int): Number of decimal places for the source token.
            destination_token_decimals (int): Number of decimal places for the destination token.
        """
        self.intent_id = intent_id
        self.source_token = source_token
        self.source_mint_address = source_mint_address
        self.source_address = source_address
        self.source_amount = source_amount
        self.destination_token = destination_token
        self.destination_mint_address = destination_mint_address
        self.destination_address = destination_address
        self.min_receive_amount = min_receive_amount
        self.partial_fill = partial_fill
        self.expiration = expiration
        self.status = status
        self.source_token_decimals = source_token_decimals
        self.destination_token_decimals = destination_token_decimals
