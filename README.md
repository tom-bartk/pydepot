<div align="center">
  <a href="https://github.com/tom-bartk/pydepot">
    <img src="https://pydepot.tombartk.com/images/logo.png" alt="Logo" width="358" height="99">
  </a>

<div align="center">
<a href="https://jenkins.tombartk.com/job/pydepot/">
  <img alt="Jenkins" src="https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Fpydepot">
</a>
<a href="https://jenkins.tombartk.com/job/pydepot/lastCompletedBuild/testReport/">
  <img alt="Jenkins tests" src="https://img.shields.io/jenkins/tests?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Fpydepot">
</a>
<a href="https://jenkins.tombartk.com/job/pydepot/lastCompletedBuild/coverage/">
  <img alt="Jenkins Coverage" src="https://img.shields.io/jenkins/coverage/apiv4?jobUrl=https%3A%2F%2Fjenkins.tombartk.com%2Fjob%2Fpydepot%2F">
</a>
<a href="https://www.gnu.org/licenses/agpl-3.0.en.html">
  <img alt="PyPI - License" src="https://img.shields.io/pypi/l/pydepot">
</a>
<a href="https://pypi.org/project/pydepot/">
  <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pydepot">
</a>
<a href="https://pypi.org/project/pydepot/">
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pydepot">
</a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;"></a>
</div>

  <p align="center">
    Strongly-typed, scalable state container for Python.
    <br />
    <a href="https://pydepot.tombartk.com"><strong>Documentation</strong></a>
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

## Installation

Pydepot is available as [`pydepot`](https://pypi.org/project/pydepot/) on PyPI:

```shell
pip install pydepot
```

## Usage

For detailed quickstart and API reference, visit the [Documentation](https://pydepot.tombartk.com/quickstart/)


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
