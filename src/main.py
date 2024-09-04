#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py
# Entry point for Mulder CLI.


import sys
import asyncio
import argparse

from src.utils.system import open_file
from src.utils.logging import log_info, log_error
from src.utils.config import load_config
from src.oracles.helius import HeliusWrapper
from src.oracles.dexscreener import DexscreenerWrapper
from src.oracles.pyth import PythWrapper
from src.sol.accounts import SolanaAccounts
from src.sol.blocks import SolanaBlocks
from src.liquidity.cexes.binance import BinanceWrapper
from src.agents.main import print_agents_list, print_agent_info
from src.agents.main import main as agent_deploy


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='Mulder CLI: Urani MEV Agent.')

    ######################################################
    #               Chains
    ######################################################
    parser.add_argument('-s', dest='solana', action='store_true',
                        help="Print info on the Solana blockchain.")

    ######################################################
    #               Agents
    ######################################################
    parser.add_argument('-a', '--agents', dest='agent', 
                        nargs= '?',const=True,
                        help="Print info on the available agents or on specific [AGENT]")

    ######################################################
    #               Deploy
    ######################################################
    parser.add_argument('-d', '--deploy', dest='deploy', 
                        nargs='?',metavar='AGENT', const=True,
                        help="Deploy a specific [AGENT].")

    ######################################################
    #               Liquidity
    ######################################################
    parser.add_argument('-l', dest='liquidity', action='store_true',
                        help="Print info on liquidity sources.")
    
    ######################################################
    #               Oracles
    ######################################################
    parser.add_argument('-o', dest='oracles', action='store_true',
                        help="Print info on the Oracles.")

    return parser


async def run() -> None:
    """Entry point for this module."""

    config = load_config()
    log_info(open_file(config['LOGO_FILE']))
    spacer = open_file(config['SPACER_FILE'])

    parser = run_menu()
    args = parser.parse_args()

    ######################################################
    #               Chains
    ######################################################
    if args.solana:
       
        log_info('\n' + spacer)
        log_info(f'Printing info on the Solana blockchain ...')
        
        token_symbol = 'SOL'
        token_mint_str = f'{token_symbol}_MINT'
        token_mint = config[token_mint_str]
        log_info(f'Token mint: {token_mint_str}\n')

        blocks = SolanaBlocks(config)
        blocks.display_blocks_info()

        accounts = SolanaAccounts(config)
        accounts.display_accounts_info(token_mint)

    ######################################################
    #               Oracles
    ######################################################
    if args.oracles:

        log_info('\n' + spacer)
        log_info(f'Printing info on the Oracles ...')

        token_symbol = 'SOL'
        token_mint_str = f'{token_symbol}_MINT'
        token_mint = config[token_mint_str]
        log_info(f'Token mint: {token_mint_str}\n')

        pyth = PythWrapper(config)
        result = await pyth.get_price_token(token_symbol)
        log_info(f'Price: {result}\n')

        dexscreen = DexscreenerWrapper(config)
        result = dexscreen.get_price_token(token_mint, token_symbol)
        log_info(f'Price: {result}\n')

        binance = BinanceWrapper(config)
        result = binance.get_price_token(token_symbol)
        log_info(f'Price: {result}\n')

        helius = HeliusWrapper(config)
        log_info(f'Price: {helius.get_price_token(token_mint)}\n')

    ######################################################
    #               Liquidity
    ######################################################
    if args.liquidity:
        log_info('\n' + spacer)
        log_info('Printing information on the Liquidity sources ...') 
        string = 'Available liquidity sources:'
        log_info(string)
        ## Jupiter
        log_info(len(string)*' ' + ' - Jupiter (https://station.jup.ag/)')

    ######################################################
    #               Agents Information
    ######################################################
    if args.agent and not args.deploy:
        log_info('\n' + spacer)
        log_info('Printing information on the Agents ...')
        if args.agent is True:
            print_agents_list()
        else:
            print_agent_info(args.agent)

    ######################################################
    #               Agent Deployment
    ######################################################
    if args.deploy:
        if args.deploy is True:
            log_error('Error: The deploy option requires an agent name.')
            parser.print_help()
            sys.exit(1)
        else:
            log_info('\n' + spacer)
            agent_name = args.deploy
            await agent_deploy(args.deploy)


    ######################################################
    #               Default
    ######################################################
    if not any(vars(args).values()):
        parser.print_help()


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
