from dataclasses import dataclass
from enum import Enum


class Commands(Enum):
    CHOICE_SERVER = 0
    SERVER_INFO = 1
    RENAME = 2
    EDIT_DESCRIPTION = 3
    EDIT_MODS = 4
    START = 5
    STOP = 6


def create_callback_data(c: int, server_id='00000', c_info=0):
    return str(server_id) + "|" + str(c) + "|" + str(c_info)


def decode_callback_data(mes):
    return mes.split("|")[0], int(mes.split("|")[1]), int(mes.split("|")[2])
