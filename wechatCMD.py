import pickle
import sys
import time
import CmdQR
from vars import pid_file, cmd_file_dir, qr_text_dir
import os
import signal


def send_signal():
    try:
        target_pid = int(open(pid_file).read().strip())
        print(target_pid)
        os.kill(target_pid, signal.SIGUSR1)
    except Exception as e:
        print(e)


def login():
    try:
        os.remove(qr_text_dir)
    except FileNotFoundError:
        pass
    with open(cmd_file_dir, 'wb') as f:
        pickle.dump({"task": "login"}, f)
    send_signal()
    while not os.path.exists(qr_text_dir):
        time.sleep(.5)
    qr_content = open(qr_text_dir).read().strip()
    print(qr_content)
    qr = CmdQR.QR(qr_content)
    qr.print_cmd_qr()


def send_file(path, to):
    with open(cmd_file_dir, 'wb') as f:
        pickle.dump({"task": "send_file", "path": path, "to": to}, f)
    send_signal()


# FIXME: currently only RemarkName available
def send_msg(msg, to):
    with open(cmd_file_dir, 'wb') as f:
        pickle.dump({"task": "msg", "msg": msg, "to": to}, f)
    send_signal()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit()
    else:
        try:
            if sys.argv[1] == "-l":
                login()
            elif sys.argv[1] == '-m':
                send_msg(sys.argv[2], sys.argv[3])
            elif sys.argv[1] == '-f':
                send_file(sys.argv[2], sys.argv[3])
        except Exception as e:
            print(e)