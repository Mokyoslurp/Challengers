"""
Format of commands to send to server are described here

"""

from enum import Enum
from typing import Union
import socket as s

from challengers.game.data import TELEMETRY

HEADER_BYTES = 3


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

    FORCE_END = 250

    RESPONSE = 255


class MessageType(Enum):
    NONE = 0
    INT = 1
    INT_LIST = 2
    STR = 3


def build_message(command: Command, data: Union[int, str, list[int]] = 0) -> tuple[bytes, bytes]:
    if isinstance(data, int):
        message_type = MessageType.INT
        message_bytes = data.to_bytes()

    elif isinstance(data, str):
        message_type = MessageType.STR
        message_bytes = data.encode()

    elif isinstance(data, list):
        message_type = MessageType.INT_LIST
        message_bytes = b"".join([d.to_bytes() for d in data])

    else:
        message_type = MessageType.NONE
        message_bytes = (0).to_bytes()

    message_length = len(message_bytes)

    if message_length <= 255:
        header_bytes = b"".join(
            [
                command.value.to_bytes(),
                message_type.value.to_bytes(),
                message_length.to_bytes(),
            ]
        )
    else:
        header_bytes = b"".join([Command.BLANK.value.to_bytes(), (1).to_bytes()])
        message_bytes = (0).to_bytes()

    return header_bytes, message_bytes


def decode_header(header: bytes) -> tuple[Command, MessageType, int]:
    try:
        command = Command(int(header[0]))
        message_type = MessageType(int(header[1]))
        message_length = int(header[2])

        return command, message_type, message_length

    except ValueError as e:
        print(e)


def decode_message(data_bytes: bytes, type: MessageType) -> Union[int, str, list[int]]:
    try:
        if type == MessageType.INT:
            data = int(data_bytes[0])

        elif type == MessageType.INT_LIST:
            data = [int(byte) for byte in data_bytes]

        elif type == MessageType.STR:
            data = data_bytes.decode()

        else:
            data = 0

        return data

    except ValueError as e:
        print(e)


def send_message(socket: s.socket, command: Command, data: Union[int, str, list[int]] = 0):
    try:
        header, message = build_message(command, data)
        socket.send(header)
        socket.send(message)

        if TELEMETRY:
            print(f"To {socket.getsockname()}: {command.name} sent with {data}")

    except s.error as e:
        print(e)


def receive_message(socket: s.socket) -> tuple[Command, Union[int, str, list[int]]]:
    try:
        header = socket.recv(HEADER_BYTES)
        command, message_type, message_length = decode_header(header)

        message = socket.recv(message_length)
        data = decode_message(message, message_type)

        if TELEMETRY:
            print(f"From {socket.getsockname()}: {command.name} received with {data}")

        return command, data

    except s.error as e:
        print(e)
