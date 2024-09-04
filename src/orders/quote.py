from typing import List, Optional, Dict, Any
# -*- encoding: utf-8 -*-
# src/orders/quote.py


class QuoteData:
    """
    Represents the details of a swap quote.

    This class encapsulates all relevant information about a token swap quote, 
    including input and output tokens, amounts, slippage, fees, and more.
    """

    def __init__(self, 
                 input_mint: str, 
                 in_amount: str, 
                 output_mint: str, 
                 out_amount: str, 
                 other_amount_threshold: str, 
                 swap_mode: str, 
                 slippage_bps: int, 
                 platform_fee: Optional[Any], 
                 price_impact_pct: str, 
                 route_plan: List[Dict[str, Any]], 
                 context_slot: int, 
                 time_taken: float):
        """
        Initialize the QuoteData object with provided attributes.

        Args:
            input_mint (str): The mint address of the input token.
            in_amount (str): The amount of input tokens.
            output_mint (str): The mint address of the output token.
            out_amount (str): The amount of output tokens.
            other_amount_threshold (str): Threshold for the other amount.
            swap_mode (str): Mode of the swap (e.g., exact input or output).
            slippage_bps (int): Slippage tolerance in basis points.
            platform_fee (Optional[Any]): Optional fee taken by the platform.
            price_impact_pct (str): Percentage of price impact.
            route_plan (List[Dict[str, Any]]): List of dictionaries detailing the swap route.
            context_slot (int): Slot number in the blockchain context.
            time_taken (float): Time taken to complete the quote process.
        """
        self.input_mint = input_mint
        self.in_amount = in_amount
        self.output_mint = output_mint
        self.out_amount = out_amount
        self.other_amount_threshold = other_amount_threshold
        self.swap_mode = swap_mode
        self.slippage_bps = slippage_bps
        self.platform_fee = platform_fee
        self.price_impact_pct = price_impact_pct
        self.route_plan = route_plan
        self.context_slot = context_slot
        self.time_taken = time_taken

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuoteData':
        """
        Create an instance of QuoteData from a dictionary.

        Args:
            data (Dict[str, Any]): A dictionary containing all the necessary attributes to initialize QuoteData.

        Returns:
            QuoteData: An instance of QuoteData initialized with the data from the dictionary.
        """
        return cls(
            input_mint=data['inputMint'],
            in_amount=data['inAmount'],
            output_mint=data['outputMint'],
            out_amount=data['outAmount'],
            other_amount_threshold=data['otherAmountThreshold'],
            swap_mode=data['swapMode'],
            slippage_bps=data['slippageBps'],
            platform_fee=data['platformFee'],
            price_impact_pct=data['priceImpactPct'],
            route_plan=data['routePlan'],
            context_slot=data['contextSlot'],
            time_taken=data['timeTaken']
        )
