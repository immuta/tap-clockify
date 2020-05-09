import singer

from dateutil.parser import parse

LOGGER = singer.get_logger()


def get_config_start_date(config):
    return parse(config.get("start_date"))
