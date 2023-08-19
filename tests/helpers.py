from contextlib import contextmanager

import pytest


@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail(f"Did raise {exception!r}")  # noqa: TRY200,TRY003
