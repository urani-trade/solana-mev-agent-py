# -*- encoding: utf-8 -*-
# src/solana/blocks.py
# Wrapper for Solana blocks methods.


import time

from src.sol.base import SolanaBase
from solana.rpc.core import RPCException
from src.utils.network import rate_limited
from src.utils.logging import log_error, log_info


class SolanaBlocks(SolanaBase):

    def __init__(self, config: dict = None, is_async: bool = False) -> None:
        super().__init__(config)

    ########################################################
    #               Public methods
    ########################################################

    @staticmethod
    def get_timestamp(block_time):
        """Returns the timestamp of a block time."""

        return time.ctime(block_time)

    @rate_limited()
    def get_slot(self) -> int:
        """Returns the current slot."""

        try:
            return self.client.get_slot().value
        except RPCException as e:
            log_error(f'RPC failure to get slot: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_block_time(self, slot: int) -> int:
        """Returns the block time."""

        try:
            return self.client.get_block_time(slot).value
        except RPCException as e:
            log_error(f'RPC failure to get block time: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_slot_leader(self) -> str:
        """Returns the slot leader."""
        try:
            return self.client.get_slot_leader().value
        except RPCException as e:
            log_error(f'RPC failure to get slot leader: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_block_height(self) -> int:
        """Returns the block height."""

        try:
            return self.client.get_block_height().value
        except RPCException as e:
            log_error(f'RPC failure to get block height: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_latest_blockhash(self, commitment=None) -> str:
        """Returns the latest blockhash."""

        try:
            lastest_blockchash = self.client.get_latest_blockhash().value
            return lastest_blockchash.blockhash
        except RPCException as e:
            log_error(f'RPC failure to get latest blockhash: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_epoch_info(self) -> dict:
        """Returns the epoch information."""

        try:
            epoch_info = self.client.get_epoch_info().value
            return {
                    "epoch": epoch_info.epoch,
                    "slot_index": epoch_info.slot_index,
                    "slots_in_epoch": epoch_info.slots_in_epoch,
                    "absolute_slot": epoch_info.absolute_slot,
                    "block_height": epoch_info.block_height
                }
        except RPCException as e:
            log_error(f'RPC failure to get epoch info: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_epoch_schedule(self) -> int:
        """Returns the epoch schedule."""

        try:
            epoch_schedule = self.client.get_epoch_schedule().value
            return {
                    "slots_per_epoch": epoch_schedule.slots_per_epoch,
                    "leader_schedule_slot_offset": epoch_schedule.leader_schedule_slot_offset,
                    "warmup": epoch_schedule.warmup,
                    "first_normal_epoch": epoch_schedule.first_normal_epoch,
                    "first_normal_slot": epoch_schedule.first_normal_slot
                }
        except RPCException as e:
            log_error(f'RPC failure to get epoch schedule: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_chain_info(self) -> dict:
        """Returns the chain information."""

        try:
            return self.client.get_cluster_nodes()
        except RPCException as e:
            log_error(f'RPC failure to get cluster nodes: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    @rate_limited()
    def get_minimum_balance_for_rent_exemption(self, data_len: int) -> int:
        """Returns the minimum balance for rent exemption."""

        try:
            return self.client.get_minimum_balance_for_rent_exemption(0).value
        except RPCException as e:
            log_error(f'RPC failure to get minimum balance for rent exemption: {e}')
        except Exception as e:
            log_error(f'Error: {e}')

    ########################################################
    #               Public methods: Helpers
    ########################################################

    def display_blocks_info(self) -> None:

        slot = self.get_slot()
        block_time = self.get_block_time(slot)
        log_info(f'Current Absolute slot: {slot}')
        log_info(f'Block time: {block_time}')
        log_info(f'Timestamp: {self.get_timestamp(block_time)}')
        log_info(f'Slot leader: {self.get_slot_leader()}')
        log_info(f'Block height: {self.get_block_height()}')
        log_info(f'Latest blockhash: {self.get_latest_blockhash()}')

        epoch_info = self.get_epoch_info()
        epoch_schedule = self.get_epoch_schedule()
        log_info(f'Epoch: {epoch_info["epoch"]}')
        log_info(f'Slot index: {epoch_info["slot_index"]}')
        log_info(f'Slots in epoch: {epoch_info["slots_in_epoch"]}')
        log_info(f'Absolute slot: {epoch_info["absolute_slot"]}')
        log_info(f'Block height: {epoch_info["block_height"]}')
        log_info(f'Slots per epoch: {epoch_schedule["slots_per_epoch"]}')
        log_info(f'Leader schedule slot offset: {epoch_schedule["leader_schedule_slot_offset"]}')
        log_info(f'Warmup: {epoch_schedule["warmup"]}')
        log_info(f'First normal epoch: {epoch_schedule["first_normal_epoch"]}')
        log_info(f'First normal slot: {epoch_schedule["first_normal_slot"]}')
