import time

import pytest

from master.node import MasterNode
from secondary.node import SecondaryNode
from shared.storage import MessageStorage
from tests.fakes import MockedTransport

DELAY_1 = 5
DELAY_2 = 6


def timed(fn, *args):
    start = time.monotonic()
    result = fn(*args)
    print(result)
    return time.monotonic() - start, result


@pytest.fixture
def cluster():
    transport = MockedTransport()
    secondary1 = SecondaryNode(MessageStorage(), "secondary-1")
    secondary2 = SecondaryNode(MessageStorage(), "secondary-2")
    transport.register("secondary-1", secondary1)
    transport.register("secondary-2", secondary2)
    master = MasterNode(transport, ["secondary-1", "secondary-2"], MessageStorage())
    return master, secondary1, secondary2, transport


def test_delayed_secondaries(cluster):
    master, secondary1, secondary2, transport = cluster

    transport.set_delay("secondary-1", DELAY_1)

    elapsed, ok = timed(master.append_message, "m1")
    print("PRINT", ok)
    # assert ok
    assert elapsed >= DELAY_1                       # blocked
    assert master.list_messages() == ["m1"]

    transport.set_delay("secondary-2", DELAY_2)

    elapsed, ok = timed(master.append_message, "m2")
    assert ok
    assert DELAY_2 <= elapsed < DELAY_1 + DELAY_2   # blocked on the slowest, sent in parallel
    assert master.list_messages() == ["m1", "m2"]

    transport.remove_delay("secondary-1")
    transport.remove_delay("secondary-2")

    elapsed, ok = timed(master.append_message, "m3")
    assert ok
    assert elapsed < 0.1                            # not blocked

    expected = ["m1", "m2", "m3"]
    assert master.list_messages() == expected
    assert secondary1.list_messages() == expected
    assert secondary2.list_messages() == expected
