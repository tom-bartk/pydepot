from collections.abc import Callable
from typing import NamedTuple
from unittest.mock import MagicMock, PropertyMock, create_autospec

import pytest

from src.pydepot import Action, Reducer, Store, StoreSubscriber
from tests.helpers import not_raises


class MockState(NamedTuple):
    value: int


class FooAction(Action):
    @property
    def value(self) -> int:
        return 42


class BarAction(Action):
    @property
    def value(self) -> int:
        raise NotImplementedError


@pytest.fixture()
def create_reducer() -> Callable[[type[Action] | None], Reducer[Action, MockState]]:
    def factory(
        action_type: type[Action] | None = None,
    ) -> Reducer[Action, MockState]:
        def apply(action, state):
            return MockState(value=action.value)

        reducer = create_autospec(Reducer)
        type(reducer).action_type = PropertyMock(return_value=action_type or FooAction)
        reducer.apply = MagicMock(side_effect=apply)

        return reducer

    return factory


@pytest.fixture()
def create_sut() -> Callable[[MockState | None], Store]:
    def factory(state: MockState | None = None) -> Store:
        return Store(initial_state=state or MockState(value=0))

    return factory


@pytest.fixture()
def create_subsciber() -> Callable[[], StoreSubscriber]:
    return lambda: create_autospec(StoreSubscriber)


class TestDispatch:
    def test_when_no_registered_reducers__does_not_raise(self, create_sut) -> None:
        sut = create_sut()
        with not_raises(Exception):
            sut.dispatch(FooAction())

    def test_when_reducer_registered_for_different_action__does_not_call_apply(
        self, create_sut, create_reducer
    ) -> None:
        reducer = create_reducer(action_type=BarAction)
        sut = create_sut()
        sut.register(reducer)

        sut.dispatch(FooAction())

        reducer.apply.assert_not_called()

    def test_when_reducer_registered_for_action__calls_apply(
        self, create_sut, create_reducer
    ) -> None:
        action = FooAction()
        state = MockState(value=0)
        reducer = create_reducer(action_type=FooAction)
        sut = create_sut(state=state)
        sut.register(reducer)

        sut.dispatch(action)

        reducer.apply.assert_called_with(action=action, state=state)

    def test_when_reducer_registered_for_action__new_state_equals_current__does_not_notify_subscribers(  # noqa: E501
        self, create_sut, create_subsciber, create_reducer
    ) -> None:
        subscriber = create_subsciber()
        reducer = create_reducer(action_type=FooAction)
        sut = create_sut(MockState(value=42))
        sut.subscribe(subscriber)
        sut.register(reducer)

        sut.dispatch(FooAction())

        subscriber.on_state.assert_not_called()

    def test_when_reducer_registered_for_action__new_state_not_equals_current__notifies_all_subscribers(  # noqa: E501
        self, create_sut, create_subsciber, create_reducer
    ) -> None:
        subscriber_1 = create_subsciber()
        subscriber_2 = create_subsciber()
        reducer = create_reducer(action_type=FooAction)
        sut = create_sut(MockState(value=0))
        sut.subscribe(subscriber_1)
        sut.subscribe(subscriber_2)
        sut.register(reducer)
        expected_new_state = MockState(value=42)

        sut.dispatch(FooAction())

        subscriber_1.on_state.assert_called_once_with(state=expected_new_state)
        subscriber_2.on_state.assert_called_once_with(state=expected_new_state)


class TestRegisterReducer:
    def test_when_action_dispatched_after_registering__apply_is_called(
        self, create_sut, create_reducer
    ) -> None:
        reducer = create_reducer(action_type=FooAction)
        sut = create_sut()

        sut.register(reducer)
        sut.dispatch(FooAction())

        reducer.apply.assert_called_once()

    def test_when_registered_same_reducer_twice__dispatching_actions_call_apply_once(
        self, create_sut, create_reducer
    ) -> None:
        reducer = create_reducer(action_type=FooAction)
        sut = create_sut()

        sut.register(reducer)
        sut.register(reducer)
        sut.dispatch(FooAction())

        reducer.apply.assert_called_once()

    def test_when_registered_two_reducers_for_same_action__dispatching_actions_call_apply_on_last_registered(  # noqa: E501
        self, create_sut, create_reducer
    ) -> None:
        reducer_1 = create_reducer(action_type=FooAction)
        reducer_2 = create_reducer(action_type=FooAction)
        sut = create_sut()

        sut.register(reducer_1)
        sut.register(reducer_2)
        sut.dispatch(FooAction())

        reducer_1.apply.assert_not_called()
        reducer_2.apply.assert_called_once()


class TestSubscribe:
    def test_when_include_current_false__does_not_notify(
        self, create_sut, create_subsciber
    ) -> None:
        sut = create_sut()
        subscriber = create_subsciber()

        sut.subscribe(subscriber, include_current=False)

        subscriber.on_state.assert_not_called()

    def test_when_include_current_true__notifies_with_current_state(
        self, create_sut, create_subsciber
    ) -> None:
        sut = create_sut()
        subscriber = create_subsciber()

        sut.subscribe(subscriber, include_current=True)

        subscriber.on_state.assert_called_once_with(state=sut.state)

    def test_when_subscribing_twice__dispatching_actions_notify_once(
        self, create_sut, create_subsciber, create_reducer
    ) -> None:
        reducer = create_reducer(action_type=FooAction)
        sut = create_sut()
        sut.register(reducer)
        subscriber = create_subsciber()

        sut.subscribe(subscriber, include_current=False)
        sut.subscribe(subscriber, include_current=False)
        sut.dispatch(FooAction())

        subscriber.on_state.assert_called_once()


class TestUnsubscribe:
    def test_when_unsubscribing_not_previously_subscribed__does_not_raise(
        self, create_sut, create_subsciber
    ) -> None:
        sut = create_sut()
        subscriber = create_subsciber()
        with not_raises(Exception):
            sut.unsubscribe(subscriber)

    def test_when_action_dispatched_after_unsubscribing__does_not_notify(
        self, create_sut, create_subsciber, create_reducer
    ) -> None:
        reducer = create_reducer(action_type=FooAction)
        subscriber = create_subsciber()
        sut = create_sut()
        sut.register(reducer)
        sut.subscribe(subscriber, include_current=False)

        sut.unsubscribe(subscriber)
        sut.dispatch(FooAction())

        subscriber.on_state.assert_not_called()

    def test_when_action_dispatched_after_unsubscribing_twice__does_not_notify(
        self, create_sut, create_subsciber, create_reducer
    ) -> None:
        reducer = create_reducer(action_type=FooAction)
        subscriber = create_subsciber()
        sut = create_sut()
        sut.register(reducer)
        sut.subscribe(subscriber, include_current=False)

        sut.unsubscribe(subscriber)
        sut.unsubscribe(subscriber)
        sut.dispatch(FooAction())

        subscriber.on_state.assert_not_called()
