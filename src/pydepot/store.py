from typing import Any, Generic, TypeVar
from weakref import WeakSet

from .abc import Action, Reducer, StoreSubscriber

__all__ = ["Store"]


TAction = TypeVar("TAction", bound=Action)
"""Invariant type variable bound by an `Action`."""

TState = TypeVar("TState")
"""Invariant type variable for a generic state."""


class Store(Generic[TState]):
    """The centralized manager of the state.

    Notifies it's subscribers whenever the state changes.

    To perform a state mutation, call the `dispatch` method with an action.
    For an action to be applied a matching reducer has to be registered first.

    Tip:
        Make sure that the reducers are registered before dispatching actions.

    """

    __slots__ = ("_reducers", "_state", "_subscribers")

    @property
    def state(self) -> TState:
        """The current state."""
        return self._state

    def __init__(self, initial_state: TState):
        """Initialize new store with a initial state.

        Args:
            initial_state (TState): The initial state.
        """
        self._reducers: dict[type[Action], Reducer[Any, TState]] = {}
        self._state: TState = initial_state
        self._subscribers: WeakSet[StoreSubscriber[TState]] = WeakSet()

    def dispatch(self, action: Action) -> None:
        """Dispatch an action to the store.

        If the dispatched action causes the state to change, all current subscribers will
        get notified by the `on_state` method.

        Before dispatching the action, make sure a `Reducer` with the matching
        `action_type` has been registered.

        Args:
            action (Action): Action to dispatch.
        """
        if reducer := self._reducers.get(type(action), None):
            new_state = reducer.apply(action=action, state=self._state)
            if new_state != self._state:
                self._state = new_state
                for subscriber in self._subscribers.copy():
                    subscriber.on_state(self._state)

    def register(self, reducer: Reducer[TAction, TState]) -> None:
        """Register a reducer.

        When an action with a type equal to `reducer.action_type` is dispatched,
        the `apply` method will be called on the `reducer` to perform the mutation.

        Registering another reducer with the same `action_type` will override the
        previous one. The store keeps a strong reference to the `reducer`.

        Args:
            reducer (Reducer[TAction, TState]): The reducer to register.
        """
        self._reducers[reducer.action_type] = reducer

    def subscribe(
        self, subscriber: StoreSubscriber[TState], include_current: bool = False
    ) -> None:
        """Subscribe to state updates.

        When the state changes, the `subscriber.on_state` will be called with the
        new state. If `include_current` is true, the subscriber is notified immediately
        with the current state.

        This method is idempotent - multiple calls will not cause multiple subscriptions.

        Make sure to keep a strong reference to the subscriber, because the store only
        keeps a weak reference.

        The `StoreSubscriber` is structurally typed, so any object implementing
        the `on_state(state: TState) -> None` method is a valid subscriber.

        Args:
            subscriber (StoreSubscriber[TState]): The subscriber to subscribe.
            include_current (bool): If true, the subscriber is immediately notified with
                the current state. If false, the first notification will happen on the
                next state change.
        """
        self._subscribers.add(subscriber)
        if include_current:
            subscriber.on_state(self._state)

    def unsubscribe(self, subscriber: StoreSubscriber[TState]) -> None:
        """Unsubscribe from state updates.

        The subscriber will no longer be notified when the state changes.

        Args:
            subscriber (StoreSubscriber[TState]): The subscriber to unsubscribe.
        """
        self._subscribers.discard(subscriber)
