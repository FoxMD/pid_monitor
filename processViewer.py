import psutil
import datetime
from tabulate import tabulate
import os
import time


def get_size(my_bytes):
    for i in ['', 'K', 'M', 'G']:
        if my_bytes < 1024:
            return f"{my_bytes:.2f}{i}B"
        my_bytes /= 1024


def get_processes():
    procs = []
    for p in psutil.process_iter():
        with p.oneshot():
            pid = p.pid
            if pid == 0:
                continue
            try:
                mem = p.memory_full_info()
            except psutil.AccessDenied:
                mem = 0
            try:
                mem_taken = p.memory_full_info().uss
                mem_taken = get_size(mem_taken)
            except psutil.AccessDenied:
                mem_taken = 0
            name = p.name()
            try:
                create_time = datetime.datetime.fromtimestamp(p.create_time())
            except OSError:
                create_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            cpu_usage = p.cpu_percent()
            try:
                cpu_affinity = len(p.cpu_affinity())
            except psutil.AccessDenied:
                cpu_affinity = 0
            status = p.status()
            try:
                user = p.username()
            except psutil.AccessDenied:
                user = 'NA'

        procs.append({
            'pid': pid,
            'name': name,
            'create time': create_time,
            'cpu usage': cpu_usage,
            'cpu affinity': cpu_affinity,
            'status': status,
            'user': user,
            'used memory': mem_taken,
            'memory': mem
        })
    return procs


def print_processes(ps):
    print(tabulate(ps, headers="keys", tablefmt="github"))


procs = get_processes()
while True:
    print_processes(procs)
    time.sleep(1)
    procs = get_processes()
    if "nt" in os.name:
        os.system("cls")
    else:
        os.system("clear")