import os
import subprocess


class Server:
    def __init__(self):
        self.work_directory = "C:\Servers"
        self.server_processes = {}

    def get_server_info(self, name):
        if name not in self.server_processes:
            return f"Сервер {name} не был запущен!"

        res = {}
        self.server_processes[name].send_signal('list')
        print(self.server_processes[name].stdout.read())

    def start_server(self, server_info):
        if server_info[0] in self.server_processes:
            return f"Сервер {server_info[1]} уже запущен!"
        if "start.bat" in os.listdir(server_info[3]):
            t = open(f"{server_info[3]}\\start.bat").read()
        else:
            t = open(f"{server_info[3]}\\run.bat").read()
        self.server_processes[server_info[0]] = subprocess.Popen(t.split('\n')[0],
                                                                 encoding="utf-8",
                                                                 cwd=f"{server_info[3]}\\",
                                                                 stdin=subprocess.PIPE,
                                                                 stdout=subprocess.PIPE,
                                                                 text=True,
                                                                 creationflags=subprocess.CREATE_NEW_CONSOLE
                                                                 )
        return f"Сервер {server_info[1]} запущен успешно!"

    def stop_server(self, server_info):
        if server_info[0] not in self.server_processes:
            return f"Сервер {server_info[1]} не был запущен!"
        self.server_processes[server_info[0]].communicate(input="stop", timeout=15)
        self.server_processes[server_info[0]].terminate()
        del self.server_processes[server_info[0]]
        return f"Сервер {server_info[1]} остановлен!"
