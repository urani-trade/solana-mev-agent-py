# -*- encoding: utf-8 -*-
# src/solana/transactions.py
# Wrapper for Solana transactions methods.


import json
import sys

from solders import message
from solana.rpc.types import TxOpts
from solders.keypair import Keypair
from solders.signature import Signature
from solana.rpc.core import RPCException
from solders.message import MessageV0
from solders.transaction import VersionedTransaction
from solders.system_program import TransferParams, transfer

from src.sol.base import SolanaBase
from src.utils.network import rate_limited
from src.utils.logging import log_debug, log_error


class SolanaTransactions(SolanaBase):

    def __init__(self, config: dict = None, is_async: bool = False) -> None:
        super().__init__(config)

    ########################################################
    #            Public methods: Solana Client
    ########################################################

    @rate_limited()
    def create_transfer_transaction(self, sender: Keypair, receiver: Keypair, amount: float) -> VersionedTransaction:
        """Creates a VersionedTransaction object for a transfer transaction."""

        tx = transfer(
            TransferParams(
                from_pubkey=sender.public_key(),
                to_pubkey=receiver.public_key(),
                lamports=self.to_lamport(amount)
            )
        )
        try:
            msg = MessageV0.try_compile(
                payer=sender.public_key(),
                instructions=[tx],
                address_lookup_table_accounts=[],
                recent_blockhash=self.get_latest_blockhash()
            )
            return VersionedTransaction(msg, [sender])
        except RPCException as e:
            log_error(f'RPC failure to create transfer transaction: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_transaction(self, tx_id: Signature) -> dict:
        """Retrieves a transaction from the Solana network."""

        try:
            response = json.loads(self.client.get_transaction(tx_id).to_json())
            if 'meta' in response['result']:
                return response['result']['meta']
            else:
                log_error(f'Transaction {tx_id} not found.')
        except RPCException as e:
            log_error(f'RPC failure to get transaction {tx_id}: {e}')
        except (KeyError, TypeError) as e:
            log_error(f'Error parsing transaction {tx_id}: {e}')
        except Exception as e:
            log_error(f'Error getting transaction {tx_id}: {e}')

    @rate_limited()
    def get_last_valid_block_height(self, commitment) -> dict:
        """Returns the last valid block height."""

        try:
            response = self.client.get_latest_blockhash(commitment=commitment).to_json()
            return json.loads(response)['result']['value']['lastValidBlockHeight']
        except RPCException as e:
            log_error(f'RPC failure to get last valid block height: {e}')
        except KeyError as e:
            log_error(f'Error parsing last valid block height: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_tx_opts(self, skip_preflight=False, preflight_commitment=None) -> dict:
        """Create a TxOpts object with the given parameters."""

        preflight_commitment = preflight_commitment or "confirmed"
        try:
            return TxOpts(skip_preflight=skip_preflight,
                     preflight_commitment=preflight_commitment,
                     last_valid_block_height=self.get_last_valid_block_height(preflight_commitment))
        except RPCException as e:
            log_error(f'RPC failure to get transaction options: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def submit_tx(self, tx: dict, opts: TxOpts) -> Signature:
        """Decode a base64 transaction, sign it, and submit it to the Solana network."""

        raw_tx = VersionedTransaction.from_bytes(self.decode_from_base64(tx))
        signature = self.keypair.sign_message(message.to_bytes_versioned(raw_tx.message))
        signed_tx = VersionedTransaction.populate(raw_tx.message, [signature])

        try:
            result = self.client.send_raw_transaction(bytes(signed_tx), opts)
            log_debug(f'TxID: {result.value}')
            return result.value
        except RPCException as e:
            log_error(f'RPC failure to submit transaction: {e}')
            return False
        except Exception as e:
            log_error(f'Error: {e}')
            return False

    @rate_limited()
    def get_tx_confirmation(self, tx_id: Signature) -> dict:
        """Get the transaction confirmation status."""

        #TODO: Implement this method
        return True
