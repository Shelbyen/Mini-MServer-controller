from enum import Enum


class Commands(Enum):
    CHOICE_SERVER = 0
    SERVER_INFO = 1
    RENAME = 2
    EDIT_DESCRIPTION = 3
    EDIT_MODS = 4
    START = 5
    STOP = 6


class ServerStatus(Enum):
    LAUNCH = 0
    READY = 1


name_server_status = {
    -1: 'Не запущен',
    0: 'Запускается',
    1: 'Запущен'
}


def create_callback_data(c: int, server_id='00000', c_info=0):
    return str(server_id) + "|" + str(c) + "|" + str(c_info)


def decode_callback_data(mes):
    return mes.split("|")[0], int(mes.split("|")[1]), int(mes.split("|")[2])


class Stub:
    def check(self, data, stdout):
        return getattr(self, data)(stdout)

    def list(self, stdout):
        data = stdout.readline()
        online_players = data[data.find('are'):].split()[1]
        max_players = data.split('of')[2].split()[0]
        players = [] if data[data.find('online:') + 8:].split(', ') == ['\n'] else data[data.find('online:') + 8:].split(', ')
        return [online_players, max_players, players]

    def tps(self, stdout):
        tps_info = stdout.readline()
        memory_info = stdout.readline()
        tps = tps_info[tps_info.rfind(':') + 2:].strip()
        use_memory = memory_info.split()[6] + ' ' + memory_info.split()[7]
        max_memory = memory_info.split()[-2] + ' ' + memory_info.split()[-1][:-1]
        return [tps, use_memory, max_memory]
