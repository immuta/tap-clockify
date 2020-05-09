#!/usr/bin/env python3

import singer

from tap_clockify.runner import ClockifyRunner
from tap_clockify.client import ClockifyClient
from tap_clockify.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=["api_key", "workspace"])
    client = ClockifyClient(args.config)
    runner = ClockifyRunner(args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == "__main__":
    main()
