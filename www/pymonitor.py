#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import subprocess
import sys

import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(level=logging.INFO)

__author__ = 'Vo7ice'


# 记录日志
def log(s):
    print('[Monitor] %s ' % s)


# 检测.py源代码改变事件
class MyFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, fn):
        super(MyFileSystemEventHandler, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source code changed: %s' % event.src_path)
            self.restart()


command = ['echo', 'ok']
process = None


# 干掉进程
def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.kill()
        process.wait()
        log('Process ended with code %s' % process.returncode)
        process = None


# 启动进程
def start_process():
    global process, command
    log('Start process %s...' % ''.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


# 重启进程 先干掉再启动
def restart_process():
    kill_process()
    start_process()


# 开始检测
def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHandler(restart_process), path, recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    argv = sys.argv[1:]
    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)
    if argv[0] != 'python':
        argv.insert(0, 'python')
    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)
