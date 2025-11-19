"""
Report Engine node base class
Defines the base interface for all processing nodes
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..llms.base import LLMClient
from ..state.state import ReportState
from loguru import logger

class BaseNode(ABC):
    """Node base class"""

    def __init__(self, llm_client: LLMClient, node_name: str = ""):
        """
        Initialize node

        Args:
            llm_client: LLM client
            node_name: Node name
        """
        self.llm_client = llm_client
        self.node_name = node_name or self.__class__.__name__
    
    @abstractmethod
    def run(self, input_data: Any, **kwargs) -> Any:
        """
        Execute node processing logic

        Args:
            input_data: Input data
            **kwargs: Additional parameters

        Returns:
            Processing result
        """
        pass

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data

        Args:
            input_data: Input data

        Returns:
            Whether validation passed
        """
        return True

    def process_output(self, output: Any) -> Any:
        """
        Process output data

        Args:
            output: Raw output

        Returns:
            Processed output
        """
        return output

    def log_info(self, message: str):
        """Record info log"""
        formatted_message = f"[{self.node_name}] {message}"
        logger.info(formatted_message)

    def log_error(self, message: str):
        """Record error log"""
        formatted_message = f"[{self.node_name}] {message}"
        logger.error(formatted_message)


class StateMutationNode(BaseNode):
    """Node base class with state modification functionality"""

    @abstractmethod
    def mutate_state(self, input_data: Any, state: ReportState, **kwargs) -> ReportState:
        """
        Modify state

        Args:
            input_data: Input data
            state: Current state
            **kwargs: Additional parameters

        Returns:
            Modified state
        """
        pass
