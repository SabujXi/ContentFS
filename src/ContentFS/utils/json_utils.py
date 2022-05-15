"""
Here are the json encoding and decoding functions.
Instead of directly using the "json" library's dumps() and loads() using these utility functions will
help to customize further like changing indentation of json output from config. Even we can switch the real
json encoding and decoding libraries.
"""
import json
from ContentFS.config import JSON_INDENT


def json_encode(data: dict, indent: int = JSON_INDENT) -> str:
    """
    Encode a dictionary into json data
    :param data: the data that will be encoded into json and be returned.
    :param indent: indentation that will be used to indent the json output.
    :return: a string as json encoded data.
    """
    return json.dumps(data, indent=indent)


def json_decode(text: str) -> dict:
    """
    Decodes a json string into python dict object.
    :param text: json data as string.
    :return: a dictionary representing data from the json text
    """
    return json.loads(text)


if __name__ == "__main__":
    print(json_encode({
        "a": 1,
        "x": {
            "y": 2
        }
    }, None))

