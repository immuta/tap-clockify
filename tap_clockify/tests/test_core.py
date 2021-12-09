"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import os

from singer_sdk.testing import get_standard_tap_tests

from tap_clockify.tap import TapClockify

SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "api_key": os.environ["TAP_CLOCKIFY_API_KEY"],
    "workspace": os.environ["TAP_CLOCKIFY_WORKSPACE"],
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapClockify, config=SAMPLE_CONFIG)
    for test in tests:
        test()
