<style>
.md-content__inner > h1:nth-child(1) {
  display: none;
}
</style>

<div align="center">
  <a href="https://github.com/tom-bartk/pydepot">
    <img src="https://pydepot.tombartk.com/images/logo-dark.png" alt="Logo" width="346" height="92">
  </a>

<div align="center">
<img alt="PyPI - License" src="https://img.shields.io/pypi/l/pydepot">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pydepot">
<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pydepot">
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
</div>

  <p align="center">
    Strongly-typed, scalable state container for Python.
    <br />
  </p>
</div>

## Simple example

```python3
# main.py

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
        return State(counter=state.counter + action.value)


class CounterSubscriber(pydepot.StoreSubscriber[State]):
    def on_state(self, state: State) -> None:
        print(f"The counter has changed to {state.counter}.")


def main() -> None:
    store = pydepot.Store(initial_state=State(counter=0))
    store.register(AddToCounterReducer())

    subscriber = CounterSubscriber()
    store.subscribe(subscriber)

    store.dispatch(AddToCounterAction(value=42))


if __name__ == "__main__":
    main()
```

```sh
$ python3 main.py

The counter has changed to 42!
```


## License
![GPLv3](https://www.gnu.org/graphics/agplv3-with-text-162x68.png)
```monospace
Copyright (C) 2023 tombartk 

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.
If not, see https://www.gnu.org/licenses/.
```
