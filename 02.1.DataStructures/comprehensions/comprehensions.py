import typing as tp


def get_unique_page_ids(records: list[tp.Mapping[str, tp.Any]]) -> set[int]:
    """
    Get unique web pages visited
    :param records: records of hit-log
    :return: Unique web pages
    """
    return {x["PageID"] for x in records}


def get_unique_page_ids_visited_after_ts(records: list[tp.Mapping[str, tp.Any]], ts: int) -> set[int]:
    """
    Get unique web pages visited after some timestamp (not included)
    :param records: records of hit-log
    :param ts: timestamp
    :return: Unique web pages visited in hit-log after some timestamp
    """
    return {x["PageID"] for x in records if x["EventTime"] > ts}


def get_unique_user_ids_visited_page_after_ts(
        records: list[tp.Mapping[str, tp.Any]],
        ts: int,
        page_id: int
        ) -> set[int]:
    """
    Get unique users visited given web page after some timestamp (not included)
    :param records: records of hit-log
    :param ts: timestamp
    :param page_id: web page identifier
    :return: Unique users visited given web page after some timestamp
    """
    return {x["UserID"] for x in records if (x["PageID"] == page_id and x["EventTime"] > ts)}

def get_events_by_device_type(
        records: list[tp.Mapping[str, tp.Any]],
        device_type: str
        ) -> list[tp.Mapping[str, tp.Any]]:
    """
    Filter events for given device type with order preservation
    :param records: records of hit-log
    :param device_type: device typy name to filter by
    :return: filtered events
    """
    return [x for x in records if x["DeviceType"] == device_type]


DEFAULT_REGION_ID = 100500


def get_region_ids_with_none_replaces_by_default(
        records: list[tp.Mapping[str, tp.Any]]
        ) -> list[int]:
    """
    Extract visited regions with order preservation. If region not defined, replace it by default region id
    :param records: records of hit-log
    :return: region ids
    """
    return [DEFAULT_REGION_ID if x["RegionID"] is None else x["RegionID"] for x in records]

def get_region_id_if_not_none(
        records: list[tp.Mapping[str, tp.Any]]
        ) -> list[int]:
    """
    Extract visited regions if they are defined with order preservation
    :param records: records of hit-log
    :return: region ids
    """
    return [x["RegionID"] for x in records if x["RegionID"] is not None]

def get_keys_where_value_is_not_none(r: tp.Mapping[str, tp.Any]) -> list[str]:
    """
    Extract keys where values are defined
    :param r: record of hit-log
    :return: keys where values are defined
    """
    return [x for x in r.keys() if r[x] is not None]


def get_record_with_none_if_key_not_in_keys(
        r: tp.Mapping[str, tp.Any],
        keys: set[str]
        ) -> dict[str, tp.Any]:
    """
    Get record with other keys replaced by None
    :param r: record of hit-log
    :param keys: keys to filter by
    :return: record with other keys replaced by None
    """
    return {x: None if x not in keys else r[x] for x in r.keys()}

def get_record_with_key_in_keys(
        r: tp.Mapping[str, tp.Any],
        keys: set[str]
        ) -> dict[str, tp.Any]:
    """
    Filter record by keys
    :param r: record of hit-log
    :param keys: keys to filter by
    :return: filtered record
    """
    return {x: r[x] for x in r.keys() if x in keys}

def get_keys_if_key_in_keys(
        r: tp.Mapping[str, tp.Any],
        keys: set[str]
        ) -> set[str]:
    """
    Filter keys from record by given keys
    :param r: record of hit-log
    :param keys: keys to filter by
    :return: filtered keys
    """
    return {x for x in r.keys() if x in keys}

