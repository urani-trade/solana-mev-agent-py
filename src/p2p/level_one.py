# -*- encoding: utf-8 -*-
# src/p2p/level_one.py
# Level one p2p network: 1 hop away.


from typing import List, Optional
from src.agents.base import AgentBase
from src.orders.intent import IntentData
from src.utils.logging import log_info


class LevelOne:

    def __init__(self):
        pass

    #####################################################
    #                  Private methods
    #####################################################

    @staticmethod
    def both_fillable(intent_1: IntentData, intent_2: IntentData) -> bool:
        """Checks if both intents can fully fill each other."""
        return (intent_1.source_amount >= intent_2.min_receive_amount and
                intent_2.source_amount >= intent_1.min_receive_amount)

    #####################################################
    #                  Public methods
    #####################################################

    def run(self, agent: AgentBase) -> List[List[IntentData]]:
        """
        P2P 1-hop away strategy using a naive neighbors search approach.

        Args:
            agent (AgentBase): The agent whose intents are to be matched.

        Returns:
            List[List[IntentData]]: A list of pairs of intents that are 1-hop away p2p matches.
        """
        p2p_matches = []
        intents = agent.batch.intents.copy()

        for i, intent_1 in enumerate(intents):
            source_1 = intent_1.source_token  
            destination_1 = intent_1.destination_token

            for j, intent_2 in enumerate(intents[i+1:], start=i+1):
                source_2 = intent_2.source_token 
                destination_2 = intent_2.destination_token 

                # Conditions check: token pair
                if (source_1 == destination_2 and destination_1 == source_2):
                    # Checks if the two intents fully overlap
                    if LevelOne.both_fillable(intent_1, intent_2):
                        p2p_matches.append([intent_1, intent_2])

        return p2p_matches if p2p_matches else []
