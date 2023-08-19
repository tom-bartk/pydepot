from abc import ABC

__all__ = ["Action"]


class Action(ABC):
    """A base class for an action.

    An action represents an intent to perfrom a state mutation.
    Defining an action is done by subclassing the `Action` with a name of the mutation.

    Example:
        Following example defines an action that, when applied, should add a `value` to
        the `counter` property of some state.
        ```python
        import pydepot

        class AddToCounterAction(pydepot.Action):
            def __init__(self, value: int):
                self.value: int = value
        ```
    """

    __slots__ = ()
