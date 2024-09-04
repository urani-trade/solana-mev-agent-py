# src/agents/aleph.py
# Aleph agent class

import asyncio

from src.agents.base import AgentBase
from src.p2p.level_one import LevelOne
from src.orders.quote import QuoteData
from src.utils.maths import calculate_surplus
from src.orders.solution import SolutionData
from src.liquidity.jupiter import JupiterWrapper
from src.utils.logging import (log_info, log_debug, log_error, 
                               exit_with_error, log_debug_object)


class Aleph(AgentBase):
    """Aleph agent."""

    def __init__(self, config: dict = None) -> None:
        super().__init__(config)
        self.name = 'Aleph'

    async def solve_order(self) -> None:
        """Solve order routine for Aleph."""

        log_info("🤙 Aleph is solving the order...\n")

        # 1- P2P
        log_info("⚙️  Searching for p2p matches ...")
        self.p2p_strategy()

        # 2- Routing 
        log_info(f'⚙️  Searching optimal execution path for {len(self.batch.intents)} intents ...')
        await self.routing()

    @classmethod
    def print_info(cls) -> None:
        """Print Agent info"""
        log_info("   Aleph is the first Urani MEV in-house agent.")
        log_info("   .Version: v0.1")
        log_info("   .Language: Python")
        log_info("   .Routing algorithm: Jupiter")
        log_info("   .P2P matches: Naive 1-hop")
        log_info("   .Partial fill: No")
        log_info("   .Ring trades: No\n")
        log_info("\n   --> Check the README to learn more about Aleph <--\n")

    def p2p_strategy(self) -> None:
        """
        Aleph p2p strategy:
        1) Naive 1-hop search.
        2) Ranking the matches according to the sum of the surplus of the two users.
        3) Eliminating redundant IDs, e.g., [(1,2), (3,4), (2,5)] -> [(1,2), (3,4)], where (1,2) has the best overall surplus.
        4) Removing from the intent list the IDs of the intents included in the p2p_matches list.
        """
        log_debug("  Checking for p2p matches ...")
    
        level_one_p2p = LevelOne()
        p2p_matches = level_one_p2p.run(self)
    
        if p2p_matches is False:
            log_info('    No p2p match found.\n')
            return
        log_info('🤙 Found p2p matches.\n')
    
        if self.config.get('LOG_LEVEL') == 'debug':
            log_debug_object('Printing all p2p matches', 'p2p match', p2p_matches)
            pass
    
        log_debug("  Ranking p2p matches ...")
        # Sort the matches based on surplus
        p2p_matches.sort(key=lambda match: 
                         calculate_surplus(match[1].source_amount,match[0].min_receive_amount) + 
                         calculate_surplus(match[0].source_amount,match[1].min_receive_amount), 
                         reverse=True)

        if self.config.get('LOG_LEVEL') == 'debug':
            log_debug_object('Printing sorted p2p matches', 'p2p match', p2p_matches)
    
        # Create the solution only for the non-repetitive intents
        log_debug("  Filtering p2p matches ...")

        processed_intent_ids = set()  # Track processed intent IDs to avoid duplicates

        # Iterate over the P2P matches
        for index,this_match in enumerate(p2p_matches):
            # Extract intents from the current match
            intent_a, intent_b = this_match

            # Skip matches involving already-processed intents
            if intent_a.intent_id in processed_intent_ids or intent_b.intent_id in processed_intent_ids:
                continue

            # Create solutions
            solution_a, solution_b = SolutionData.from_intent_match(intent_a, intent_b)

            # Set the id: we start from 1
            id = 2*index
            solution_a.solution_id = f"{id+1}"
            solution_b.solution_id = f"{id+2}"
            
            # Add solutions to the batch
            self.batch.solutions[f'{id+1}'] = solution_a
            self.batch.solutions[f'{id+2}'] = solution_b

            # Add intent IDs to the processed set
            processed_intent_ids.update({intent_a.intent_id, intent_b.intent_id})

        log_debug(" Removing processed intents from the batch...")
        # Filter out processed intents from the batch
        self.batch.intents = [
            intent for intent in self.batch.intents 
            if intent.intent_id not in processed_intent_ids
        ]
        if self.config.get('LOG_LEVEL') == 'debug':
            log_debug_object('Printing reamining intents to match', 'intent', self.batch.intents)
    
    async def routing(self) -> None:
        """
        Perform routing to get quotes and create solutions for remaining intents.
        
        This involves:
        1. Fetching quotes for each intent from Jupiter.
        2. Creating solutions based on the quotes.
        """
        
        # Get quotes from Jupiter
        quotes = await self.get_jupiter_quotes()

        # Craft and append solutions
        id = len(self.batch.solutions)
        for index, quote in enumerate(quotes):

            solution = SolutionData.from_quote(quote, self.batch.intents[index])

            # We enumerate the first solutions as "1" and not "0"
            solution.solution_id = f"{id+1}"
            self.batch.solutions[id+1] = solution
            id+=1
    
    async def get_jupiter_quotes(self) -> list[QuoteData]:
        """
        Retrieve quotes from Jupiter with retry logic.
        Returns:
            list: A list of quotes retrieved from Jupiter.
        """
        jupiter = JupiterWrapper(self.config)
        max_retries = self.MULDER_MAX_INSTANCES
        retry_delay = self.MULDER_UPDATE_SECONDS

        for attempt in range(1, max_retries + 1):
            try:
                # Run concurrently a different jupiter routing for each intent
                quotes = await asyncio.gather(*[jupiter.get_quote(intent) for intent in self.batch.intents])
                return [QuoteData.from_dict(quote) for quote in quotes]  
            
            except Exception as e:
                log_error(f"  Retrieving quotes from Jupiter, attempt #{attempt} failed: {str(e)}")
                if attempt < max_retries:
                    log_error(f"  Retrying in {retry_delay} second(s)...")
                    await asyncio.sleep(retry_delay)  # Wait before retrying
                else:
                    exit_with_error("  Maximum retry attempts reached. Failing operation.")

if __name__ == '__main__':
    Aleph().run()
