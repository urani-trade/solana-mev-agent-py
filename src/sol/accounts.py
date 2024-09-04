# -*- encoding: utf-8 -*-
# src/solana/accounts.py
# Wrapper for Solana account methods.


import json

from solders.pubkey import Pubkey
from src.sol.base import SolanaBase
from solana.rpc.core import RPCException
from src.utils.network import rate_limited
from solana.rpc.types import TokenAccountOpts
from src.utils.logging import log_error, log_info


class SolanaAccounts(SolanaBase):

    def __init__(self, config: dict = None, is_async: bool = False) -> None:
        super().__init__(config)

    ########################################################
    #               Public methods: Helpers
    ########################################################

    def get_token_decimals(self, token_address: str) -> int:
        """Returns the decimals of a token."""

        data = self.get_account_info(token_address)
        try:
            return 10 ** data['result']['value']['data']['parsed']['info']['decimals']
        except KeyError as e:
            log_error(f'Error parsing data: {e}')
            return 0

    def get_token_lamports(self, token_address: str) -> int:
        """Returns the lamports of a token."""

        data = self.get_account_info(token_address)
        try:
            return data['result']['value']['lamports']
        except KeyError as e:
            log_error(f'Error parsing data: {e}')
            return 0


    def get_token_mint_authority(self, token_address: str) -> str:
        """Returns the mint authority of a token."""

        data = self.get_account_info(token_address)
        try:
            return data['result']['value']['data']['parsed']['info']['mintAuthority']
        except KeyError as e:
            log_error(f'Error parsing data: {e}')
            return 0

    def get_token_supply(self, token_address: str) -> int:
        """Returns the supply of a token."""

        data = self.get_account_info(token_address)
        try:
            return data['result']['value']['data']['parsed']['info']['supply']
        except KeyError as e:
            log_error(f'Error parsing data: {e}')
            return 0

    def get_token_owner(self, token_address: str) -> str:
        """Returns the owner of a token."""

        data = self.get_account_info(token_address)
        try:
            return data['result']['value']['owner']
        except KeyError as e:
            log_error(f'Error parsing data: {e}')
            return 0

    def is_account_executable(self, token_address: str) -> bool:
        """Returns whether an account is executable."""

        data = self.get_account_info(token_address)
        try:
            return data['result']['value']['executable']
        except KeyError as e:
            log_error(f'Error parsing data: {e}')

    def get_token_balance(self, token_address: str) -> float:
        """Returns the token balance of a wallet."""

        response = json.loads(self.get_token_accounts_by_owner(token_address))
        if response['result']['value'] == []:
            log_error(f'Could not find token balance for {token_address}')
        else:
            try:
                return response['result']['value'][0]['account']['data']['parsed']['info']['tokenAmount']['uiAmount']
            except RPCException as e:
                log_error(f'RPC failure to get token balance: {e}')
            except Exception as e:
                log_error(f'Error: {e}')
        return 0

    @rate_limited()
    def get_sol_balance(self, pubkey: str) -> float:
        """Returns the balance of SOl in a wallet."""

        try:
            return self.from_lamports(self.client.get_balance(pubkey).value)
        except RPCException as e:
            log_error(f'RPC failure to get balance: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    ########################################################
    #               Public methods: PDAs
    ########################################################

    def check_if_pda(self, address: str) -> bool:
        """
            Checks if an address is a program-derived address.
            (i.e., th address does not have a private key).
        """
        return not self.get_pubkey_object(address).is_on_curve()

    ########################################################
    #            Public methods: Solana Client
    ########################################################

    @rate_limited()
    def get_token_accounts_by_owner(self, token_address) -> dict:
        """Returns the token accounts of a wallet."""

        opts = TokenAccountOpts(mint=Pubkey.from_string(token_address))
        try:
            return self.client.get_token_accounts_by_owner_json_parsed(self.pubkey, opts).to_json()
        except RPCException as e:
            log_error(f'RPC failure to get token accounts: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_account_info(self, token_address: str) -> dict:
        """Returns the account information of a wallet."""

        try:
            return json.loads(self.client.get_account_info_json_parsed(Pubkey.from_string(token_address)).to_json())
        except RPCException as e:
            log_error(f'RPC failure to get account info: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_token_mint_account(self, token_address: str) -> Pubkey:

        try:
            return self.client.get_associated_token_address(self.pubkey, Pubkey.from_string(token_address))
        except RPCException as e:
            log_error(f'RPC failure to get token mint account: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    ########################################################
    #               Public methods: Helpers
    ########################################################

    def display_accounts_info(self, token_address) -> None:

        log_info(f'Sol_balance: {self.get_sol_balance(self.pubkey)}')
        log_info(f'Token balance for {token_address}: {self.get_token_balance(token_address)}')
        log_info(f'Token Decimals: {self.get_token_decimals(token_address)}')
        log_info(f'Token Mint authority: {self.get_token_mint_authority(token_address)}')
        log_info(f'Token Supply: {self.get_token_supply(token_address)}')
        log_info(f'Token Owner: {self.get_token_owner(token_address)}')
        log_info(f'Is account executable: {self.is_account_executable(token_address)}')
