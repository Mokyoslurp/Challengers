"""
Format of commands to send to server are described here

"""

from enum import Enum

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
    END_CARD_MANAGEMENT = 39

    FORCE_END = 255


def build_request(command: Command, data: int):
    if data < 255:
        message = (command.value << 8) + data
        return message.to_bytes(REQUEST_BYTES)
    return (0).to_bytes(REQUEST_BYTES)


def build_response(data: int):
    if data < 255:
        return data.to_bytes(RESPONSE_BYTES)
    return (0).to_bytes(RESPONSE_BYTES)


def decode_request(request: bytes):
    try:
        data = int(request[1])
        command = Command(int(request[0]))
        return command, data
    except ValueError as e:
        return e


def decode_response(response: bytes):
    try:
        data = int(response[0])
        return data
    except ValueError as e:
        return e
