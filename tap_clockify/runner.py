import json
import singer
import sys

from tap_clockify.state import save_state


LOGGER = singer.get_logger()


class ClockifyRunner:
    def __init__(self, args, client, available_streams):
        self.available_streams = available_streams
        self.catalog = args.catalog
        self.client = client
        self.config = args.config
        self.state = args.state

    def get_streams_to_replicate(self):
        streams = []

        if not self.catalog:
            return streams

        for stream_catalog in self.catalog.streams:
            if not is_selected(stream_catalog):
                LOGGER.info(
                    "'%s' is not marked selected, skipping.", stream_catalog.stream
                )
                continue

            for available_stream in self.available_streams:
                if available_stream.matches_catalog(stream_catalog):
                    if not available_stream.requirements_met(self.catalog):
                        raise RuntimeError(
                            "%s requires that that the following are selected: %s",
                            stream_catalog.stream,
                            ",".join(available_stream.REQUIRES),
                        )

                    to_add = available_stream(
                        self.config, self.state, stream_catalog, self.client
                    )

                    streams.append(to_add)

        return streams

    def do_discover(self):
        LOGGER.info("Starting discovery.")

        catalog = []

        for available_stream in self.available_streams:
            stream = available_stream(self.config, self.state, None, None)

            catalog += stream.generate_catalog()

        json.dump({"streams": catalog}, sys.stdout, indent=4)

    def do_sync(self):
        LOGGER.info("Starting sync.")

        streams = self.get_streams_to_replicate()

        for stream in streams:
            try:
                stream.state = self.state
                stream.sync()
                self.state = stream.state
            except OSError as e:
                LOGGER.error(str(e))
                exit(e.errno)

            except Exception as e:
                LOGGER.error(str(e))
                LOGGER.error("Failed to sync endpoint %s, moving on!", stream.TABLE)
                raise e

        save_state(self.state)


def is_selected(stream_catalog):
    metadata = singer.metadata.to_map(stream_catalog.metadata)
    stream_metadata = metadata.get((), {})

    inclusion = stream_metadata.get("inclusion")

    if stream_metadata.get("selected") is not None:
        selected = stream_metadata.get("selected")
    else:
        selected = stream_metadata.get("selected-by-default")

    if inclusion == "unsupported":
        return False

    elif selected is not None:
        return selected

    return inclusion == "automatic"
