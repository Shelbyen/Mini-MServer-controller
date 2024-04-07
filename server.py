import os
import subprocess
from queue import Queue
from threading import Thread

from other import ServerStatus, Stub


class Server:
    def __init__(self, process):
        self.server_process = process
        self.status = ServerStatus.LAUNCH.value
        self.commands = Queue(5)
        self.info = {'players': ['0', '0', []],
                     'TPS': ['', '', '']}
        Thread(target=self.wait_start, daemon=True).start()
        self.read_server = Thread(target=self._read_server, daemon=True)
        self.stop_thread = False

    def wait_start(self):
        while True:
            output = self.server_process.stdout.readline()
            if output == '' and self.server_process.poll() is not None or 'For help, type "help"' in output:
                print('Server launched!')
                break
        self.status = ServerStatus.READY.value
        self.read_server.start()
        self.add_command('list')
        self.add_command('tps')

    def stop_server(self):
        self.stop_thread = True
        if self.read_server:
            self.read_server.join()
        self.server_process.communicate(input="stop", timeout=15)
        self.server_process.terminate()

    def add_command(self, command):
        if self.status != ServerStatus.READY.value:
            return False
        self.commands.put(command)

    def _read_server(self):
        while True:
            if self.stop_thread:
                break
            if self.commands.empty():
                continue
            command = self.commands.get()
            self.server_process.stdin.write(command + '\n')
            self.server_process.stdin.flush()
            data = Stub().check(command, self.server_process.stdout)
            self.info['players' if command == 'list' else 'TPS'] = data


class ServerController:
    def __init__(self):
        self.work_directory = r"C:\Servers"
        self.server_processes = {}

    def get_server_info(self, info):
        if info[0] not in self.server_processes:
            return f"Сервер {info[1]} не был запущен!"
        self.server_processes[info[0]].add_command('list')
        self.server_processes[info[0]].add_command('tps')
        return self.server_processes[info[0]].info

    def start_server(self, server_info):
        if server_info[0] in self.server_processes:
            return f"Сервер {server_info[1]} уже запущен!"

        if "start.bat" in os.listdir(server_info[3]):
            t = open(f"{server_info[3]}\\start.bat").read()
        else:
            t = open(f"{server_info[3]}\\run.bat").read()
        self.server_processes[server_info[0]] = Server(subprocess.Popen(t.split('\n')[0],
                                                                        encoding="utf-8",
                                                                        cwd=f"{server_info[3]}\\",
                                                                        stdin=subprocess.PIPE,
                                                                        stdout=subprocess.PIPE,
                                                                        text=True,
                                                                        universal_newlines=True,
                                                                        creationflags=subprocess.CREATE_NEW_CONSOLE
                                                                        ))
        return f"Сервер {server_info[1]} запущен успешно!"

    def stop_server(self, server_info):
        if server_info[0] not in self.server_processes:
            return f"Сервер {server_info[1]} не был запущен!"
        self.server_processes[server_info[0]].stop_server()
        del self.server_processes[server_info[0]]
        return f"Сервер {server_info[1]} остановлен!"
