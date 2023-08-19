from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from .action import Action

__all__ = ["Reducer"]


TAction = TypeVar("TAction", bound=Action)
"""Invariant type variable bound by an `Action`."""

TState = TypeVar("TState")
"""Invariant type variable for a generic state."""


class Reducer(Generic[TAction, TState], ABC):
    """A base class for a reducer.

    Reducer performs state mutations by applying an action to the current state.
    Defining a reducer is done by subclassing the `Reducer` and specyfing the type of
    action it should handle.

    Example:
        Following example defines a reducer for the `AddToCounterAction`, that adds
        the `action.value` to the `State.counter`.

        ```python
        from typing import NamedTuple

        import pydepot


        class State(NamedTuple):
            counter: int


        class AddToCounterAction(pydepot.Action):
            def __init__(self, value: int):
                self.value: int = value


        class AddToCounterReducer(pydepot.Reducer[AddToCounterAction, State]):
            @property
            def action_type(self) -> type[AddToCounterAction]:
                return AddToCounterAction

            def apply(self, action: AddToCounterAction, state: State) -> State:
                return State(counter=state.counter + action.value)  # The mutation.
        ```
    """

    __slots__ = ()

    @property
    @abstractmethod
    def action_type(self) -> type[TAction]:
        """The type of an action that this reducer handles."""

    @abstractmethod
    def apply(self, action: TAction, state: TState) -> TState:
        """Apply an action to the current state.

        The `Store` calls this method when an action is dispatched. The return value
        should be the state after applying the mutation described by the action.

        Args:
            action (TAction): The action to apply.
            state (TState): The current state.

        Returns:
            TState: The state after applying the action.
        """
