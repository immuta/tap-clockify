import json
import singer

from dateutil.parser import parse

LOGGER = singer.get_logger()


def get_last_record_value_for_table(state, table):
    last_value = singer.bookmarks.get_bookmark(state, table, "last_record")

    if last_value is None:
        return None

    return parse(last_value)


def incorporate(state, table, field, value):
    if value is None:
        return state

    new_state = state.copy()

    parsed = parse(value).strftime("%Y-%m-%dT%H:%M:%SZ")

    if "bookmarks" not in new_state:
        new_state["bookmarks"] = {}

    last_record = singer.bookmarks.get_bookmark(new_state, table, "last_record")
    if last_record is None or last_record < value:
        new_state = singer.bookmarks.write_bookmark(new_state, table, field, parsed)

    return new_state


def save_state(state):
    if not state:
        return

    LOGGER.info("Updating state.")

    singer.write_state(state)


def load_state(filename):
    if filename is None:
        return {}

    try:
        return singer.utils.load_json(filename)
    except:
        LOGGER.fatal("Failed to decode state file. Is it valid json?")
        raise RuntimeError
