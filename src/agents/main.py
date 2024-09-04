#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/mulder/main.py
# Entry point for each Agent

import sys
import asyncio
import argparse

from src.agents.aleph import Aleph
from src.utils.logging import log_info
from src.utils.config import load_config
from src.agents.base import AgentBase


def print_agents_list() -> None:
    """
    Print the list of available MEV agents.

    This function logs the names of all available MEV agents that can be deployed.
    Currently, it lists only the Aleph agent, but more agents can be added in the future.
    """
    info_string = 'List of available MEV Agents: '
    log_info(info_string)
    log_info(' ' * len(info_string) + '- Aleph (v0.1 - Python)')


def print_agent_info(agent_name: str, deploy: bool = False) -> None:
    """
    Print information about a specific agent, optionally indicating if it's being deployed.

    This function provides information on the specified agent. If the `deploy` flag is set 
    to True, it logs a message indicating that the agent is being deployed.

    Args:
        agent_name (str): The name of the agent.
        deploy (bool, optional): If True, indicates that the agent is being deployed. Defaults to False.

    Raises:
        SystemExit: If the agent name is not recognized.
    """
    if deploy: 
        log_info(f'🛹 Deploying Agent {agent_name.capitalize()} ...')
    else:
        log_info(f'\nRequesting information about Agent {agent_name.capitalize()} ...\n')

    # Check if the requested agent is Aleph and print its info
    if agent_name.lower() == 'aleph':
        Aleph.print_info()
    else:
        log_info(f"Agent '{agent_name}' not recognized.")
        print_agents_list()  # Print the available agents if the specified one is not found
        sys.exit(1)


async def main(agent_name: str) -> None:
    """
    Main entry point for running the specified agent.

    This function initializes and runs the specified agent. It loads the necessary 
    configuration settings, prints agent information, and starts the agent's execution.

    Args:
        agent_name (str): The name of the agent to run.
    """
    config = load_config()  # Load configuration settings
    log_info("Loading environment variables...\n")
    
    # Print information on the agent being deployed
    print_agent_info(agent_name, deploy=True)

    # Initialize the agent class based on the agent_name
    agent_class = AgentBase.initialize_agent(agent_name)
    agent = agent_class()

    # Run the agent
    log_info(f"🛹 Starting Agent {agent.name}...")
    await agent.run()

    log_info(f"\n🛹 Agent {agent.name} has finished\n")


if __name__ == "__main__":
    # Argument parser for the command line to specify the agent name
    parser = argparse.ArgumentParser(description="Run the agent.")
    parser.add_argument('agent_name', type=str, help='The name of the agent to run')
    args = parser.parse_args()
 
    # Run the main function with the provided agent name
    asyncio.run(main(args.agent_name))
