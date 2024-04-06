import os
import subprocess
from time import sleep


class Server:
    def __init__(self):
        self.work_directory = "C:\Servers"
        self.server_processes = {}

    def get_servers(self):
        res = {}
        for i in os.listdir(self.work_directory):
            if i != "build tools":
                if "readme.txt" in os.listdir(f"{self.work_directory}\\{i}"):
                    res[i] = open(f"{self.work_directory}\\{i}\\readme.txt", 'r', encoding='utf-8').read()
                else:
                    res[i] = 'Нет описания('
        return res

    def get_server_info(self, name):
        if name not in self.server_processes:
            return f"Сервер {name} не был запущен!"

        res = {}
        self.server_processes[name].send_signal('list')
        print(self.server_processes[name].stdout.read())

    def start_server(self, name):
        if name not in self.server_processes:
            if "start.bat" in os.listdir(f"{self.work_directory}\\{name}"):
                t = open(f"{self.work_directory}\\{name}\\start.bat").read()
            else:
                t = open(f"{self.work_directory}\\{name}\\run.bat").read()
            self.server_processes[name] = subprocess.Popen(t.split(),
                                                           encoding="utf-8",
                                                           cwd=f"{self.work_directory}\\{name}",
                                                           stdin=subprocess.PIPE,
                                                           stdout=subprocess.PIPE,
                                                           text=True,
                                                           creationflags=subprocess.CREATE_NEW_CONSOLE
                                                           )
            return f"Сервер {name} запущен успешно!"
        else:
            return f"Сервер {name} уже запущен!"

    def stop_server(self, name):
        if name not in self.server_processes:
            return f"Сервер {name} не был запущен!"
        self.server_processes[name].communicate(input="stop", timeout=15)
        self.server_processes[name].terminate()
        del self.server_processes[name]
        return f"Сервер {name} остановлен!"


a = Server()
a.start_server('server_i')
sleep(25)
a.get_server_info('server_i')
