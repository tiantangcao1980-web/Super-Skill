def add(a, b):
    """Implements: User request: Build a calculator  --- Intent Contract --- ## Intent Contract (st"""
    return a + b


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0


# Exit conditions met:
# - acceptance items pass
# - one unit test present
# - implementation is self-contained

