from abc import abstractmethod
from typing import Protocol, TypeVar

__all__ = ["StoreSubscriber"]


TState = TypeVar("TState", contravariant=True)
"""Contravariant type variable for a generic state."""


class StoreSubscriber(Protocol[TState]):
    """The protocol for a store subscriber.

    Any object implementing the `on_state(state: TState) -> None` method
    is a valid subscriber.
    """

    @abstractmethod
    def on_state(self, state: TState) -> None:
        """Notify the subscriber of a state change.

        If the subscriber is currently subscribed to a `Store`, this method is called
        every time the state changes.

        Args:
            state (TState): The new state.
        """
