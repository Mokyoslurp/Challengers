"""
Format of commands to send to server are described here

"""

from enum import Enum
from typing import Union

REQUEST_BYTES = 2
REQUEST_LENGTH = 8 * REQUEST_BYTES

RESPONSE_BYTES = 1
RESPONSE_LENGTH = 8 * RESPONSE_BYTES


# Hexadecimal from 0x00 to 0xFF -> 0-255
class Command(Enum):
    BLANK = 0

    # Server commands
    CONNECT = 1
    LEAVE = 2

    # Game preparation commands
    READY = 10

    # Duel commands
    PLAY_CARD = 20

    # Card management commands
    DRAW_CARD = 30
    DISCARD_CARD = 31
    END_CARD_MANAGEMENT = 39

    # Get self player properties commands
    GET_SELF_DECK = 41
    GET_SELF_BENCH = 42
    GET_SELF_PLAYED_CARDS = 43

    # Get opponent player properties commands
    GET_OPPONENT_BENCH = 52
    GET_OPPONENT_PLAYED_CARDS = 53

    GET_STATUS = 60

    FORCE_END = 255


def build_request(command: Command, data: int):
    if data < 255:
        message = (command.value << 8) + data
        return message.to_bytes(REQUEST_BYTES)
    return (0).to_bytes(REQUEST_BYTES)


def build_response(data: Union[int, list[int]], length: int = 1):
    if not isinstance(data, list):
        data = [data]

    data_bytes = b""
    for d in list[int](data):
        if d < 255:
            data_bytes += d.to_bytes(RESPONSE_BYTES)
        else:
            data_bytes += (0).to_bytes(RESPONSE_BYTES)

    length_byte = length.to_bytes(RESPONSE_BYTES)
    return length_byte, data_bytes


def decode_request(request: bytes):
    try:
        data = int(request[1])
        command = Command(int(request[0]))
        return command, data
    except ValueError as e:
        return e


def decode_response(response: bytes):
    try:
        data = []
        for byte in response:
            data.append(int(byte))
        return data
    except ValueError as e:
        return e
