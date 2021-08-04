#!/usr/bin/env python3
#
# TP-Link Wi-Fi Smart Plug Protocol Client
# For use with TP-Link HS-100 or HS-110
#
# by Lubomir Stroetmann
# Copyright 2016 softScheck GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import socket
import json
from struct import pack

version = 0.4

# Check if hostname is valid
def validHostname(hostname):
    try:
        socket.gethostbyname(hostname)
    except socket.error:
        parser.error("Invalid hostname.")
    return hostname

# Check if port is valid
def validPort(port):
    try:
        port = int(port)
    except ValueError:
        parser.error("Invalid port number.")

    if ((port <= 1024) or (port > 65535)):
        parser.error("Invalid port number.")

    return port


# Predefined Smart Plug Commands
# For a full list of commands, consult tplink_commands.txt
# powers = {   'high'     : 15,
#             'mid'      : 0,
#             'low'      : -15
# }

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171

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


# Parse commandline arguments
parser = argparse.ArgumentParser(description=f"TP-Link Wi-Fi Smart Plug Client v{version}")
parser.add_argument("-t", "--target", metavar="<hostname>", required=True,
                    help="Target hostname or IP address", type=validHostname)
parser.add_argument("-p", "--port", metavar="<port>", default=9999,
                    required=False, help="Target port", type=validPort)
parser.add_argument("-q", "--quiet", dest="quiet", action="store_true",
                    help="Only show result")

parser.add_argument("-f", "--file", dest="file", action="store_true",
                   help="Load JSON string from the file")
parser.add_argument("--timeout", default=10, required=False,
                    help="Timeout to establish connection")

# parser.add_argument("-o", "--power", metavar="<power>",
#                    help="Preset power levels to send. Choices are: "+", ".join(powers), choices=powers)



def send_cmd(cmd, ip, port, timeout, quiet):
    # Send command and receive reply
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.settimeout(int(timeout))
        sock_tcp.connect((ip, port))
        sock_tcp.settimeout(None)
        

        #print(cmd)
        #print(encrypt(cmd))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()

        decrypted = decrypt(data[4:])

        if quiet:
            print(decrypted)
        else:
            print("Sent:     ", cmd)
            print("Received: ", decrypted)

    except socket.error:
        quit(f"Could not connect to host {ip}:{port}")


def make_schedule_cmd(smin, sact, schedule):
    schedule["schedule"]["add_rule"]["smin"] = smin
    schedule["schedule"]["add_rule"]["sact"] = sact
    out = str(schedule)
    out = out.replace("'", "\"") # must be using single quote
    return out

def get_percentage(f):
    return (60 - f) / 67

# ourside tempture + 13 ~ inside temprature
# def get_hourly_interval(hour_int, temp):
#     # hour_int 10PM = 20*60 = 1200    
#     hour_in_mins = hour_int * 60
#     percentage = get_percentage(temp)
#     if percentage < 0.09:
#         return (hour_in_mins, hour_in_mins)
#     elif percentage < 0.15:
#         return (hour_in_mins, hour_in_mins+15)
#     elif percentage < 0.30:
#         return (hour_in_mins, hour_in_mins+30)
#     elif percentage < 0.40:        
#         return (hour_in_mins, hour_in_mins+45)
#     elif percentage < 0.50:        
#         return (hour_in_mins, hour_in_mins+50)   
#     else:
#         return (hour_in_mins, hour_in_mins+60)

# ourside tempture + 13 ~ inside temprature
def get_hourly_interval(hour_int, temp):
    # hour_int 10PM = 20*60 = 1200    
    hour_in_mins = hour_int * 60
    if temp >= 54:
        return (hour_in_mins, hour_in_mins)
    if temp >= 50:
        return (hour_in_mins, hour_in_mins+15)
    elif temp >= 40:
        return (hour_in_mins, hour_in_mins+30)
    elif temp >= 30:        
        return (hour_in_mins, hour_in_mins+45)
    elif temp >= 27:        
        return (hour_in_mins, hour_in_mins+50)   
    else:
        return (hour_in_mins, hour_in_mins+60)


args = parser.parse_args()

#MID
intervals = [(1290, 30), (90, 150), (210, 270), (330, 390), (450, 510), (600, 660)]
temps = [(22, 51),
         (23, 50),
         (0, 50),
         (1, 50),
         (2, 50),
         (3, 50),
         (4, 51),
         (5, 52),
         (6, 52),
         (7, 54),
         (8, 55),
         (9, 56),
         (10, 58),
         (11, 60),
         (12, 60)
        ]

def filter_and_combine(intervals):
    non_none_intervals = [(s, e) for (s, e) in intervals if (s!=e)]
    
    out = []
    start_s = 0
    new = True
    
    for start, end in [(s, e) for (s, e) in non_none_intervals if s!=e]:
        if new:
            start_s = start
        if end != start + 60:
            out.append((start_s, end))
            new = True
        else:
            new = False
    return out


#high +15
#low -15

# Set target IP, port and command to send
ip = args.target
port = args.port
if  args.file is not None:

    with open('rule.json') as f:
        schedule = json.load(f)
        #erase all existing schedule
        send_cmd('{"schedule":{"delete_all_rules":null,"erase_runtime_stat":null}}', ip, port, args.timeout, args.quiet)
        
        intervals = [get_hourly_interval(hour_int, temp) for (hour_int, temp) in temps]
        #print(intervals)

        clean_intervals = filter_and_combine(intervals)
        for start, end in clean_intervals:
            start_cmd = make_schedule_cmd(start, 1, schedule)
            end_cmd = make_schedule_cmd(end, 0, schedule)

            send_cmd(start_cmd, ip, port, args.timeout, args.quiet)
            send_cmd(end_cmd, ip, port, args.timeout, args.quiet)
            
# elif args.command is None:
#     cmd =args.json
# else:
#     cmd = commands[args.command]


