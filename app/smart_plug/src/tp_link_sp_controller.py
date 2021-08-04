import socket
import json
from struct import pack

# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
schedule_json = """
{
    "schedule": {
        "add_rule": {
            "stime_opt": 0,
            "wday": [
                1,
                1,
                1,
                1,
                1,
                1,
                1
            ],
            "smin": 0,
            "enable": 1,
            "repeat": 1,
            "etime_opt": -1,
            "name": "lights on",
            "eact": -1,
            "month": 0,
            "sact": 0,
            "year": 0,
            "longitude": 0,
            "day": 0,
            "force": 0,
            "latitude": 0,
            "emin": 0
        },
        "set_overall_enable": {
            "enable": 1
        }
    }
}
"""

def encrypt(string):
    key = 171
    result = pack(">I", len(string))
    for i in string:
        a = key ^ ord(i)
        key = a
        result += bytes([a])
    return result

def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ i
        key = i
        result += chr(a)
    return result


def load_schedule_from_json():
    with open('rule.json') as f:
        schedule = json.load(f)
        return schedule


def load_schedule_from_str():
    schedule = json.loads(schedule_json)
    return schedule


def make_schedule_cmd(smin, sact):
    if smin >= 1440:
        smin -= 1440
    #schedule = load_schedule_from_json()
    schedule = load_schedule_from_str()
    schedule["schedule"]["add_rule"]["smin"] = smin
    schedule["schedule"]["add_rule"]["sact"] = sact
    out = str(schedule)
    out = out.replace("'", "\"") # must be using single quote
    return out


def send_cmd(cmd, ip, port=9999, timeout=10, verbase=False):
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.settimeout(int(timeout))
        sock_tcp.connect((ip, port))
        sock_tcp.settimeout(None)

        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()
        decrypted = decrypt(data[4:])

        if verbase:
            print("Sent:     ", cmd)
            print("Received: ", decrypted)

    except socket.error:
        quit(f"Could not connect to host {ip}:{port}")


def send_schedule_cmd(smin, sact, ip):
    cmd = make_schedule_cmd(smin, sact)
    send_cmd(cmd, ip)


def clean_schedule(ip):
    send_cmd('{"schedule":{"delete_all_rules":null,"erase_runtime_stat":null}}', ip)

