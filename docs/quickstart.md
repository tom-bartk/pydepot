## Define the State

A state is an object that keeps track of some properties of a system. Example of such property can be a simple boolean flag such as `has_accepted_cookies`, or a list of objects rendered on the screen. It should be immutable, so that only the store can perform mutations.

Following example defines a state class, that tracks the current value of a counter:

```python3
from typing import NamedTuple


class State(NamedTuple):
    counter: int
```

Subclassing the [`NamedTuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) ensures immutability, while providing attribute lookup.

## Define an Action

An [`Action`](/api/action/#pydepot.abc.Action) is an object representing an intent to perform some mutation on the state.

Following example defines an action that, when applied, should add some value to the counter:

```python3
import pydepot


class AddToCounterAction(pydepot.Action):
    def __init__(self, value: int):
        self.value: int = value
```

## Add a Reducer

For the `AddToCounterAction` to have any meaning, it needs a reducer that will perform the actual mutation. A [`Reducer`](/api/reducer/#pydepot.abc.Reducer) is an object that produces a new state by applying an action to the current state.

Following example defines a reducer for the `AddToCounterAction`:

```python3
import pydepot


class AddToCounterReducer(pydepot.Reducer[AddToCounterAction, State]):
    @property
    def action_type(self) -> type[AddToCounterAction]:
        return AddToCounterAction

    def apply(self, action: AddToCounterAction, state: State) -> State:
        return State(counter=state.counter + action.value)
```

The `apply` method will be called by the `Store` when an `AddToCounterAction` is dispatched.

## Create a Subscriber

Pydepot offers a useful way for any object to be notified whenever a state changes, similar to the Pub/Sub design pattern. A subscriber is an object that implements the [`on_state(self, state: TState) -> None`](/api/subscriber/#pydepot.abc.subscriber.StoreSubscriber.on_state) method defined in the [`StoreSubscriber[TState]`](/api/subscriber/#pydepot.abc.StoreSubscriber) protocol.

Following example defines a subscriber, that prints the current value of the counter:

```python3
import pydepot


class CounterSubscriber(pydepot.StoreSubscriber[State]):
    def on_state(self, state: State) -> None:
        print(f"The counter has changed to {state.counter}.")
```

The `pydepot.StoreSubscriber[State]` does not need to be included in the MRO, as the typing of the subscriber is checked structurally.

## Create the Store

The [`Store`](/api/store/#pydepot.Store) is the central manager of the state. You can perform state mutations by dispatching actions to it. Objects can also subscribe to be notified whenever the state changes.


Following example creates the store, registers the `AddToCounterReducer`, and subscribes the `CounterSubscriber`:

```python3
import pydepot


def main() -> None:
    store = pydepot.Store(initial_state=State(counter=0))
    store.register(AddToCounterReducer())

    subscriber = CounterSubscriber()
    store.subscribe(subscriber)

if __name__ == "__main__":
    main()
```

## Dispatch an Action

The final step is to perform the state mutation by dispatching an action.


Following example dispatches the `AddToCounterAction` to the store, which will add `42` to the current value of the counter:

```python3
def main() -> None:
    ...
    store.dispatch(AddToCounterAction(value=42))

```

Running the script will result in the `CounterSubscriber` reacting to the state change:

```sh
$ python3 main.py

The counter has changed to 42!
```

<hr/>
To learn more, see the [API Documentation](/api/store/).
<br/>
