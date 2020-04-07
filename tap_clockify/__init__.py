#!/usr/bin/env python3

import singer
import tap_framework

from tap_clockify.client import ClockifyClient
from tap_clockify.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


class ClockifyRunner(tap_framework.Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=['api-key', 'workspace'])
    client = ClockifyClient(args.config)
    runner = ClockifyRunner(args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()