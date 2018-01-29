import pickle
import signal

import time

from vars import cmd_file_dir

from wechatAPI import WechatAPI

api = WechatAPI()


def do_exit(sig, stack):
    raise SystemExit('Exiting')


def start_task(sig, stack):
    cmd = read_cmd()
    if cmd['task'] == "login":
        api.login()
    elif cmd['task'] == "send_file":
        api.send_file(cmd["path"], cmd["to"])

    elif cmd['task'] == "msg":
        api.send_msg(cmd["msg"], cmd["to"])
    elif cmd['task'] == "get_friend":
        api.get_friend(cmd['target'])
    elif cmd['task'] == "reset":
        api.reset()


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
