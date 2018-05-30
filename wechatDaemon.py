import pickle
import signal

import time

from vars import cmd_file_dir

from wechatAPI import WechatAPI

api = WechatAPI()


# DEPENDENCY( pid )

def do_exit(sig, stack):
    raise SystemExit('Exiting')


def start_task(sig, stack):
    cmd = read_cmd()
    if cmd['task'] == "login":
        api.login()
    elif cmd['task'] == "send_file":
        api.append_task("file", cmd["path"], cmd["to"])
    elif cmd['task'] == "msg":
        api.append_task("msg", cmd["msg"], cmd["to"])


def read_cmd():
    with open(cmd_file_dir, "rb") as f:
        cmd = pickle.load(f)
    print(cmd)
    return cmd


signal.signal(signal.SIGINT, do_exit)
signal.signal(signal.SIGUSR1, start_task)

if __name__ == '__main__':
    from pid import PidFile
    from pid import PidFileAlreadyLockedError

    try:
        with PidFile(piddir='/tmp/'):  # TODO: may inconsistent with var in vars.py
            while True:
                time.sleep(1)
    except PidFileAlreadyLockedError:
        pass
