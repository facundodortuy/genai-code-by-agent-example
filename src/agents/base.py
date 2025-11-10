"""Base agent class and common functionality."""
import uuid
from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Base class for all AI agents."""

    def __init__(self, name: str, role: str):
        """Initialize the agent.

        Args:
            name: Agent name
            role: Agent role description
        """
        self.name = name
        self.role = role
        self.agent_id = str(uuid.uuid4())

    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process input and return output.

        Args:
            input_data: Input data to process

        Returns:
            Processed output
        """
        pass

    def generate_id(self) -> str:
        """Generate a unique ID."""
        return str(uuid.uuid4())

    def log(self, message: str) -> None:
        """Log a message from this agent.

        Args:
            message: Message to log
        """
        print(f"[{self.name}] {message}")
