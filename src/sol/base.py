# -*- encoding: utf-8 -*-
# src/solana/base.py
# Base class for Solana wrappers.


import base64
import base58

from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from src.utils.config import load_config, log_debug


class SolanaBase:

    def __init__(self, config: dict = None, is_async: bool = False) -> None:

        self.config = config or load_config()
        self.rpc_https = self.config['SOLANA_RPC_HTTPS']
        self.privkey = self.config['WALLET_PRIVATE_KEY']

        self.keypair = self.get_keypair(self.privkey)
        self.pubkey = self.get_pubkey(self.keypair)

        if is_async:
            self.client = self.get_async_client(self.rpc_https)
        else:
            self.client = self.get_client(self.rpc_https)

    ########################################################
    #               Public methods: Connection
    ########################################################

    def get_client(self, rps_https: str) -> Client:
        """Returns a client object for the Solana RPC."""

        log_debug(f'Starting Solana client at {rps_https}...')
        return Client(rps_https)

    def get_async_client(self, rps_https: str) -> AsyncClient:
        """Returns an async client object for the Solana RPC."""

        log_debug('Starting Solana async client at {rps_https}...')
        log_debug('Warning: Most of the methods are not async yet.')
        return AsyncClient(rps_https)

    def get_key_from_bytes(self, key: bytes) -> str:
        """Returns a key from bytes."""

        return Keypair.from_bytes(key)

    def get_keypair(self, privkey: str) -> Keypair:
        """Returns a keypair object from a private key."""

        return self.get_key_from_bytes(self.decode_from_base58(privkey))

    def get_pubkey(self, keypair: Keypair) -> str:
        """Returns the public address of the wallet."""

        return keypair.pubkey()

    def get_pubkey_object(self, address: str) -> Pubkey:
        """Returns a pubkey object."""

        return Pubkey.from_string(address)

    ########################################################
    #            Static methods
    ########################################################

    @staticmethod
    def decode_from_base64(key: str) -> bytes:
        """Decodes a key from base64 string."""

        return base64.b64decode(key)

    @staticmethod
    def encode_to_base64(key: bytes) -> str:
        """Encodes a key to base64 string."""

        return base64.b64encode(key).decode()

    @staticmethod
    def decode_from_base58(key: str) -> bytes:
        """Decodes a key from base58."""

        return base58.b58decode(key)

    @staticmethod
    def encode_to_base58(key: bytes) -> str:
        """Encodes a key to base58."""

        return base58.b58encode(key).decode()

    @staticmethod
    def from_lamports(amount: float) -> int:
        """Converts an amount to lamports."""

        return float(amount / 10 ** 9)

    @staticmethod
    def to_lamport(amount: int) -> float:
        """Converts an amount from lamports."""
        return float(amount * 10 ** 9)
