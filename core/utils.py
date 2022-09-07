import os
import logging
import cuid
import arrow
import uuid
import decimal
from core import hash_utils


def get_logger_by_name(logger_name):
    LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
    logger = logging.getLogger(name=logger_name)
    logger.setLevel(LOGLEVEL)
    return logger

def iso_utc_now():
    return str(arrow.utcnow())


def arrow_utc_now():
    return arrow.utcnow()

def generate_unique_id():
    """
    https://github.com/ericelliott/cuid
    Collision-resistant ids optimized for horizontal scaling and performance.

    Consists of 25 alphanumeric characters (letters are always lowercase)
    Always starts with a (lowercase) letter, e.g. c
    Follows cuid (collision resistant unique identifiers) scheme
    """
    return cuid.cuid()

def make_workspace_secret():
    return uuid.uuid4().hex


def make_short_id(string_or_number):
    # TODO: maybe change this to cuid.slug()
    return hash_utils.encode_id(string_or_number)

def object_sanitizer(obj):
    """
    There seems to be no method for DynamoDb TypeSerializer overrides
    """
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = object_sanitizer(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = object_sanitizer(v)
        return obj
    elif isinstance(obj, set):
        return list(object_sanitizer(i) for i in obj)
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj
